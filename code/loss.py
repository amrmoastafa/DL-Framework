import numpy as np
import sys
import math
from activations import softMax
from abstract_classes import Function

class Loss(Function):
    def __init__(self,*args, **kwargs):
        super().__init__()
    
    def forward(self, Y_hat, Y):
        pass
    def calculate_local_grads(self, Y_hat, Y):
        pass
    def backward(self):
        return self.local_grads["x"]
        
class MeanSquareLoss(Loss):
  def forward(self, Y_hat, Y):
    return (Y_hat-Y)**2
  
  def calculate_local_grads(self, Y_hat, Y):
    # dL_dYhat = (2 * (Y_hat - Y))
    # m_examples = dL_dYhat.shape[0]
    # return {'x': dL_dYhat / m_examples }
    return {'x' : 2*(Y_hat - Y) }
  

class CrossEntropyLoss(Loss):
    def forward(self, Y_hat, Y):
        """
            new

            yhat = (ndim, nbatch)
            y = (1, nbatch)
        """
        probs = softMax(Y_hat)
        # print(probs)
        # print()
        y = Y.T

        log_probs = -np.log([(probs[y[i], i]+1e-10) for i in range(probs.shape[1])])
        

        #  ........... Problem ...............
        # Y is inf because y hat at the begin is very big (range 8k) so e^8k = inf 
        crossentropy_loss = max(np.mean(log_probs), 0) # avrage on both axis 0 & axis 1 ()
        # crossentropy_loss = np.sum(crossentropy_loss, axis=1, keepdims=True)
        #print("Dims", probs.shape)
        
        print('Label =',Y)
        print('Pred  = ',np.argmax(probs,axis=0))

        # caching for backprop
        self.cache['probs'] = probs
        self.cache['y'] = Y
        if math.isnan(crossentropy_loss):
            sys.exit(0)
        return crossentropy_loss

    def calculate_local_grads(self, X, Y):
        probs = self.cache['probs']
        b = np.zeros((probs.shape[1],probs.shape[0]))
        b[np.arange(Y.shape[1]),Y] = 1
        b = b.T
        probs = np.subtract(probs,b) / float(Y.shape[0])
        # probs = np.sum(probs, axis=1, keepdims=True)

        #probs =  probs.mean(axis=1,keepdims=True)
        # print("back loss")
        # print(probs.shape)
        # print("What is X ?")
        # print(X.shape)
        return {'x':probs}

            
            

