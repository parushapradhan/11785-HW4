import numpy as np

class Linear:
    def __init__(self, in_features, out_features):
        """
        Initialize the weights and biases with zeros
        W shape: (out_features, in_features)
        b shape: (out_features,)  # Changed from (out_features, 1) to match PyTorch
        """
        # DO NOT MODIFY
        self.W = np.zeros((out_features, in_features))
        self.b = np.zeros(out_features)


    def init_weights(self, W, b):
        """
        Initialize the weights and biases with the given values.
        """
        # DO NOT MODIFY
        self.W = W
        self.b = b

    def forward(self, A):
        """
        :param A: Input to the linear layer with shape (*, in_features)
        :return: Output Z with shape (*, out_features)
        
        Handles arbitrary batch dimensions like PyTorch
        """
        # TODO: Implement forward pass
        
        # Store input for backward pass
        input_shape = self.W.shape[1]
        bacth_size = np.prod(A.shape[0:A.ndim - 1])
        
        A_reshaped = A.reshape(bacth_size, input_shape)
        
        Z = np.dot(A_reshaped, self.W.T) + self.b
        # Reshape Z to match the input shape of A
        Z = Z.reshape(A.shape[0:-1] + (self.W.shape[0],))
        self.A = A
        
        return Z

    def backward(self, dLdZ):
        """
        :param dLdZ: Gradient of loss wrt output Z (*, out_features)
        :return: Gradient of loss wrt input A (*, in_features)
        """
        # TODO: Implement backward pass
        dLdZ_reshaped = dLdZ.reshape(-1, self.W.shape[0])
        # Compute gradients (refer to the equations in the writeup)
        self.dLdA = np.dot(dLdZ_reshaped, self.W)
        self.dLdW = np.dot(dLdZ_reshaped.T, self.A.reshape(-1, self.W.shape[1]))
        self.dLdb = np.sum(dLdZ_reshaped, axis=0)
        self.dLdA = self.dLdA.reshape(self.A.shape)
        
        # Return gradient of loss wrt input
        return self.dLdA
