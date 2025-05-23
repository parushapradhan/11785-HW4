import numpy as np


class Softmax:
    """
    A generic Softmax activation function that can be used for any dimension.
    """
    def __init__(self, dim=-1):
        """
        :param dim: Dimension along which to compute softmax (default: -1, last dimension)
        DO NOT MODIFY
        """
        self.dim = dim

    def forward(self, Z):
        """
        :param Z: Data Z (*) to apply activation function to input Z.
        :return: Output returns the computed output A (*).
        """
        if self.dim > len(Z.shape) or self.dim < -len(Z.shape):
            raise ValueError("Dimension to apply softmax to is greater than the number of dimensions in Z")
        
        # TODO: Implement forward pass
        # Compute the softmax in a numerically stable way
        # Apply it to the dimension specified by the `dim` parameter
        A = np.exp(Z - np.max(Z, axis=self.dim, keepdims=True)) / np.sum(np.exp(Z - np.max(Z, axis=self.dim, keepdims=True)), axis=self.dim, keepdims=True)
        self.A = A
        return A

    # def backward(self, dLdA):
    #     """
    #     :param dLdA: Gradient of loss wrt output
    #     :return: Gradient of loss with respect to activation input
    #     """
    #     # TODO: Implement backward pass
        
    #     # Get the shape of the input
    #     shape = self.A.shape
    #     # Find the dimension along which softmax was applied
    #     C = shape[self.dim]
           
    #     # Reshape input to 2D
    #     if len(shape) > 2:
    #         self.A = NotImplementedError
    #         dLdA = NotImplementedError

    #     # Reshape back to original dimensions if necessary
    #     if len(shape) > 2:
    #         # Restore shapes to original
    #         self.A = NotImplementedError
    #         dLdZ = NotImplementedError

    #     raise NotImplementedError
    def backward(self, dLdA):
        """
        :param dLdA: Gradient of loss wrt output
        :return: Gradient of loss with respect to activation input
        """
        # TODO: Implement backward pass
 
        # Get the original shape
        shape = self.A.shape
        C = shape[self.dim]  # Find the dimension along which softmax was applied

        # Move softmax dimension to the last axis to simplify calculations
        A_moved = np.moveaxis(self.A, self.dim, -1)  # Shape (..., C)
        dLdA_moved = np.moveaxis(dLdA, self.dim, -1)  # Shape (..., C)

        # Flatten all dimensions except for the softmax axis
        new_shape = (-1, C)  # Reshape into (batch_size, C)
        A_flat = A_moved.reshape(new_shape)
        dLdA_flat = dLdA_moved.reshape(new_shape)

        # Initialize dLdZ with the same shape
        dLdZ_flat = np.zeros_like(A_flat)

        # Compute the Jacobian and the gradient per batch element
        for i in range(A_flat.shape[0]):
            # Construct the Jacobian matrix (C x C)
            J = np.zeros((C, C))
            for m in range(C):
                for n in range(C):
                    if m == n:
                        J[m, n] = A_flat[i, m] * (1 - A_flat[i, n])
                    else:
                        J[m, n] = -A_flat[i, m] * A_flat[i, n]

            # Compute dLdZ[i] = dLdA[i] @ J (Shape: (1, C) * (C, C) → (1, C))
            dLdZ_flat[i, :] = dLdA_flat[i, :] @ J

        # Reshape back to the original moved shape
        dLdZ_moved = dLdZ_flat.reshape(A_moved.shape)

        # Move the softmax axis back to its original position
        dLdZ = np.moveaxis(dLdZ_moved, -1, self.dim)
            
        return dLdZ
 

    