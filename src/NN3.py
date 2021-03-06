import numpy as np
from nn_utils import sigmoid

learning_rate = 0.001


class NN3:
    def __init__(self, dataset, epochs, w=None, print_step=None):
        self.train_x, self.test_x, self.train_y, self.test_y = dataset
        self.l3_error = 0
        self.neurons = self.train_x.shape[1]
        self.Xavier = 1  # np.sqrt(1.0 / 2 * self.neurons)
        if w is None:
            self.w0 = (2 * np.random.random((self.neurons, self.neurons)) - 1) * self.Xavier
            self.w1 = (2 * np.random.random((self.neurons, self.neurons)) - 1) * self.Xavier
            self.w2 = (2 * np.random.random((self.neurons, 1)) - 1) * self.Xavier
        else:
            self.w0, self.w1, self.w2 = w[0], w[1], w[2]
        for j in xrange(1, epochs + 1):
            l1 = sigmoid(np.dot(self.train_x, self.w0))
            l2 = sigmoid(np.dot(l1, self.w1))
            l3 = sigmoid(np.dot(l2, self.w2))
            self.l3_error = self.train_y - l3

            if (print_step is not None) and (
                    (j % print_step == 0) or j == epochs):
                accuracy, acc_std = self.calc_accuracy()
                print("{},{},{},{}".format(j, np.mean(np.abs(self.l3_error)), accuracy, acc_std))

            l3_adjustment = self.l3_error * sigmoid(l3, deriv=True)
            l2_error = l3_adjustment.dot(self.w2.T)

            l2_adjustment = l2_error * sigmoid(l2, deriv=True)
            l1_error = l2_adjustment.dot(self.w1.T)

            l1_adjustment = l1_error * sigmoid(l1, deriv=True)

            # dropout of 10%
            # self._drop_out(self.W2, DROPOUT_RATE)

            # update weights for all the synapses (no learning rate term)
            self.w2 += l2.T.dot(l3_adjustment) * learning_rate
            self.w1 += l1.T.dot(l2_adjustment) * learning_rate
            self.w0 += self.train_x.T.dot(l1_adjustment) * learning_rate

    def get_weights(self):
        return [self.w0, self.w1, self.w2]

    def get_error(self):
        return np.mean(np.abs(self.l3_error))

    def calc_accuracy(self):
        l1 = sigmoid(np.dot(self.test_x, self.w0))
        l2 = sigmoid(np.dot(l1, self.w1))
        l3 = sigmoid(np.dot(l2, self.w2))
        y_error = self.test_y - l3
        return 1 - np.mean(np.abs(y_error)), np.std(y_error)
