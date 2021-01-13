"""
A federated learning client with support for Adaptive Parameter Freezing (APF).

Reference:

C. Chen, et al. "Communication-Efficient Federated Learning with Adaptive Parameter Freezing"

"""
import copy
import torch

from models import registry as models_registry
from trainers import registry as trainers_registry
from config import Config
from clients import SimpleClient
from clients.simple import Report


class APFClient(SimpleClient):
    """A federated learning client with Adaptive Parameter Freezing."""
    async def train(self):
        """Adaptive Parameter Freezing will be applied after training the model."""
        # Preserve the model before training for rolling back frozen parameters
        self.trainer.preserve_weights()

        # Perform model training
        self.trainer.train(self.trainset)

        # Extract model weights and biases
        weights = self.trainer.extract_weights()

        # Generate a report for the server, performing model testing if applicable
        if Config().clients.do_test:
            accuracy = self.trainer.test(self.testset, 1000)
        else:
            accuracy = 0

        return Report(self.client_id, len(self.data), weights, accuracy)