from config import AirTaxi
import random
import numpy as np

def sim_data_generate(data_size, obstacle_aug_size, obstacles_prob=0.8, action_keep_prob=0.8):
    
    def observe_formulas(args, formulas):
        return all(formula(args) for formula in formulas)
    
    action_predicates = AirTaxi().action_predicate
    observed_predicates = AirTaxi().observed_predicate
    past_action_predicates = AirTaxi().past_action_predicate
    predicate_num = AirTaxi().constants['total_action_num'] + AirTaxi().constants['condition_num']
    action_predicate_num = len(action_predicates)
    observed_predicate_num = len(observed_predicates)
    formula_set = AirTaxi().formulas
    simulated_data=[]
    
    options = [
        ('Cruising', 'Landing'),
        ('Altitude_above_50', 'Altitude_below_50'),
        ('Velocity_less_than_2', 'Velocity_more_than_2')
    ]

    for action, action_index in action_predicates.items():
        num = 0
        print(action)
        while num < data_size:
            fakedata = [0] * (predicate_num)
            fakedata[action_index] = 1
            for option1, option2 in options:
                if random.random() < 0.5:
                    fakedata[observed_predicates[option1]] = 1
                else:
                    fakedata[observed_predicates[option2]] = 1
                        
            if random.random() < obstacles_prob:
                fakedata[observed_predicates['Obstacles_in_1m_radius']] = 1
                
            # Check if adding this predicate violates any formulas
            if observe_formulas(fakedata, formula_set):
                if action == 'Stop' and fakedata[observed_predicates['Obstacles_in_1m_radius']] == 1:
                    fakedata[random.choice(list(past_action_predicates.values()))] = 1
                else:
                    if random.random() < action_keep_prob:
                        fakedata[action_index+action_predicate_num+observed_predicate_num] = 1
                    else:
                        past_action_index = random.choice(list(past_action_predicates.values()))
                        fakedata[past_action_index] = 1
                simulated_data.append(fakedata)
                num+=1
                
    for i in range(obstacle_aug_size):
        fakedata = [0] * (predicate_num)
        fakedata[observed_predicates['Obstacles_in_1m_radius']] = 1
        for option1, option2 in options:
            if random.random() < 0.5:
                fakedata[observed_predicates[option1]] = 1
            else:
                fakedata[observed_predicates[option2]] = 1
        fakedata[action_predicates['Stop']] = 1
        fakedata[random.choice(list(past_action_predicates.values()))] = 1
        simulated_data.append(fakedata)
                
    return simulated_data

    

if __name__ == "__main__":
    data = sim_data_generate(1000,1000)
    np.save("sim_data.npy", data)
    print(len(data))