import numpy as np
from scipy.special import softmax
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_satisfaction(data, formulas):
    satisfaction_counts = np.zeros((len(data), len(formulas)))
    for i, instance in enumerate(data):
        for j, formula in enumerate(formulas):
            satisfaction_counts[i, j] = formula(instance)
    return satisfaction_counts

def log_sum_exp(x):
    max_x = np.max(x)
    return max_x + np.log(np.sum(np.exp(x - max_x)))

def compute_log_likelihood(satisfaction_counts, weights, regularization):
    weighted_sum = satisfaction_counts @ weights
    log_likelihood = np.sum(weighted_sum) - log_sum_exp(weighted_sum)
    log_likelihood -= 0.5 * regularization * np.sum(weights ** 2)  # L2 regularize
    return log_likelihood

def update_weights(weights, satisfaction_counts, learning_rate, regularization):
    weighted_sum = satisfaction_counts @ weights
    expected_satisfaction = np.exp(weighted_sum - log_sum_exp(weighted_sum))
    gradient = np.sum(satisfaction_counts, axis=0) - np.sum(expected_satisfaction[:, None] * satisfaction_counts, axis=0)
    gradient -= regularization * weights
    weights += learning_rate * gradient
    return weights

def compute_accuracy(true_labels, predictions):
    return np.mean(true_labels == predictions)


class MLN:
    
    def __init__(self, config, weights=None, learning_rate=0.01, max_iter=100, tol=1e-6, regularization=0.01):
        self.formulas = config.formulas
        self.constants = config.constants
        # self.possible_worlds = config.possible_worlds
        if weights is not None:
            self.weights = weights
        else:
            self.weights = np.ones(len(self.formulas))
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.regularization = regularization

    def train_mln(self, data, saving_path):
        """
        data: np.array([...])
        """   
        weights = self.weights
        prev_log_likelihood = -np.inf
        prev_acc = -np.inf
        

        for iteration in range(self.max_iter):
            satisfaction_counts = compute_satisfaction(data, self.formulas)
            log_likelihood = compute_log_likelihood(satisfaction_counts, weights, self.regularization)
            header = 0
            avg_prob = 0
            for idx, action_num_entity in enumerate(self.constants['action_type']):
                true_labels = np.argmax(data[:, header: header+action_num_entity[1]], axis=1)
                header += action_num_entity[1]
                predictions_prob = []
                for instance in data:
                    condition_input = instance[self.constants['total_action_num']:]
                    probs, _ = self.infer_action_probability(condition_input)
                    action_probs = probs[idx]
                    predictions_prob.append(action_probs[true_labels[len(predictions_prob)]])
                avg_prob += np.mean(predictions_prob)
            avg_prob /= len(self.constants['action_type'])
            logger.info(f"Iteration {iteration}, Average Probability of Ground Truth Action: {avg_prob}, Log Likelihood: {log_likelihood}")
            if np.abs(log_likelihood - prev_log_likelihood) < self.tol:
                np.save(saving_path, weights)
                logger.info("log likelihood converged.")
                break
            if np.abs(avg_prob - prev_acc) < self.tol:
                np.save(saving_path, weights)
                logger.info("accuracy converged.")
                break
            if avg_prob > prev_acc:
                prev_acc = avg_prob
                np.save(saving_path, weights)
                logger.info(f"Saving weights at iteration {iteration}")
            prev_log_likelihood = log_likelihood
            weights = update_weights(weights, satisfaction_counts, self.learning_rate, self.regularization)
            self.weights = weights
        return weights
    
    def generate_possible_instances(self, condition_input, action_num, condition_num):
        possible_instances = []
        possible_worlds = list(range(action_num))
        for pw in possible_worlds:
            instance = np.zeros(action_num + condition_num)
            instance[action_num:] = condition_input 
            instance[pw] = 1
            possible_instances.append(instance)
        return np.array(possible_instances) 
    

    def infer_action_probability(self, condition_input):
        possible_instances = self.generate_possible_instances(condition_input, self.constants['total_action_num'], self.constants['condition_num'])
        satisfaction_counts = compute_satisfaction(possible_instances, self.formulas)
        log_probs = satisfaction_counts @ self.weights
        header = 0
        probs = []
        indices = []
        for action_num_entity in self.constants['action_type']:
            prob = softmax(log_probs[header: header+action_num_entity[1]])
            probs.append(prob)
            indices.append(np.argmax(prob)+header)
            header += action_num_entity[1]
        return probs, indices
    
    
    def validate_instance(self, instance):
        violations = []
        for idx, formula in enumerate(self.formulas):
            if formula(instance) != 1:
                violations.append(idx)
        return violations
    
    
    def compute_instance_probability(self, instance):
        condition_input = instance[self.constants['total_action_num']:]
        probs, _ = self.infer_action_probability(condition_input)
        instance_probs = []
        header = 0
        for idx, action_num_entity in enumerate(self.constants['action_type']):
            instance_probs.append(probs[idx][instance[header: header+action_num_entity[1]].argmax()])
            header += action_num_entity[1]
        return instance_probs
