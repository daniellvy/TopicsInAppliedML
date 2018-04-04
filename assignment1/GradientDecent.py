import numpy as np


class Parameters(object):
    def __init__(self, steps, alpha):
        super(Parameters, self).__init__()
        self.steps = steps
        self.alpha = alpha


def LearnModelFromDataUsingSGD(data, mfmodel, parameters):

    for step in range(parameters.steps):
        xs, ys = data.nonzero()
        for x, y in zip(xs, ys):
            sample = (x, y, data[x, y])
            gradient_decent_update(sample, mfmodel, parameters)

        predicted = calc_matrix(mfmodel)
        print("Step: %s, error: %f" % (step, mean_squared_error(data, predicted)))


def gradient_decent_update(sample, mfmodel, parameters):
    i = sample[0]
    j = sample[1]

    # Calculate error
    prediction = mfmodel.mu + mfmodel.b_m[i] + mfmodel.b_n[j] + np.dot(mfmodel.u[i, :], mfmodel.v[j, :])
    e = sample[2] - prediction

    # Update user and movie latent feature matrices
    temp_u = mfmodel.u[i, :]
    mfmodel.u[i, :] -= parameters.alpha * (-1 * e * mfmodel.v[j, :] + mfmodel.lamb.lambda_u * mfmodel.u[i, :])
    mfmodel.v[j, :] -= parameters.alpha * (-1 * e * temp_u + mfmodel.lamb.lambda_v * mfmodel.v[j, :])

    # Update biases
    mfmodel.b_m[i] -= parameters.alpha * (-1 * e + mfmodel.lamb.lambda_b_u * mfmodel.b_m[i])
    mfmodel.b_n[j] -= parameters.alpha * (-1 * e + mfmodel.lamb.lambda_b_v * mfmodel.b_n[j])

    if  mfmodel.b_m[i] > 200 or  mfmodel.b_m[i] < -200:
        print(mfmodel.b_m[i])

    if e > 200 or e < -200:
        print(sample)
        print(e)



def calc_matrix(mfmodel):
    return (mfmodel.mu + mfmodel.b_n[:, np.newaxis] + mfmodel.b_m[np.newaxis, :]).T + mfmodel.u.dot(mfmodel.v.T)


def mean_squared_error(data, predicted):
    xs, ys = data.nonzero()
    error = 0
    for x, y in zip(xs, ys):
        error += pow(data[x, y] - predicted[x, y], 2)
    return np.sqrt(error)
