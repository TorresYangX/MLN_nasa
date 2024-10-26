from MLN import MLN
from config import AirTaxi
import numpy as np

class trainer:
    def __init__(self, data_path):
        self.config = AirTaxi()
        self.train_data = np.load(data_path)
        self.learning_rate = 1e-5
        self.regularization = 1e-5
        self.max_iter = 10000
        
    def train(self):
        mln = MLN(self.config, learning_rate=self.learning_rate, max_iter=self.max_iter, regularization=self.regularization)
        mln.train_mln(self.train_data, "weights.npy")
        
if __name__ == "__main__":
    trainer = trainer("NASA/sim_data.npy")
    trainer.train()