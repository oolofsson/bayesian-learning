#!/usr/bin/python
# coding: utf-8

# # Lab 3: Bayes Classifier and Boosting

# ## Jupyter notebooks
#
# In this lab, you can use Jupyter <https://jupyter.org/> to get a nice layout of your code and plots in one document. However, you may also use Python as usual, without Jupyter.
#
# If you have Python and pip, you can install Jupyter with `sudo pip install jupyter`. Otherwise you can follow the instruction on <http://jupyter.readthedocs.org/en/latest/install.html>.
#
# And that is everything you need! Now use a terminal to go into the folder with the provided lab files. Then run `jupyter notebook` to start a session in that folder. Click `lab3.ipynb` in the browser window that appeared to start this very notebook. You should click on the cells in order and either press `ctrl+enter` or `run cell` in the toolbar above to evaluate all the expressions.

# ## Import the libraries
#
# In Jupyter, select the cell below and press `ctrl + enter` to import the needed libraries.
# Check out `labfuns.py` if you are interested in the details.

import numpy as np
from scipy import misc
from imp import reload
from labfuns import *
import random


# ## Bayes classifier functions to implement
#
# The lab descriptions state what each function should do.

# find the number of occurences of k within the list labels
def findKCount(labels, k):
    count = 0;
    for i in range(0,len(labels)):
        if labels[i] == k:
            count = count + 1
    return count

# NOTE: you do not need to handle the W argument for this part!
# in: labels - N vector of class labels
# out: prior - C x 1 vector of class priors
def computePrior(labels, W=None):
    Npts = labels.shape[0]
    if W is None:
        W = np.ones((Npts,1))/Npts
    else:
        assert(W.shape[0] == Npts)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    prior = np.zeros((Nclasses,1))

    for i in range(0,len(prior)):
        prior[i] = findKCount(labels, i)/len(labels)
    return prior

def computePrior2(labels, W):
    Npts = labels.shape[0]
    if W is None:
        W = np.ones((Npts,1))/Npts
    else:
        assert(W.shape[0] == Npts)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    prior = np.zeros((Nclasses,1))

    i = 0
    while i < Npts:
        li = labels[i]
        prior[li] += np.sum(W[li])
        i += 1

    prior /= np.sum(W)

    return prior

# NOTE: you do not need to handle the W argument for this part!
# in:      X - N x d matrix of N data points
#     labels - N vector of class labels
# out:    mu - C x d matrix of class means (mu[i] - class i mean)
#      sigma - C x d x d matrix of class covariances (sigma[i] - class i sigma)
def mlParams(X, labels, W=None):
    assert(X.shape[0]==labels.shape[0])
    Npts,Ndims = np.shape(X)
    classes = np.unique(labels) # fetches all unique elements from labels
    Nclasses = np.size(classes)

    if W is None:
        W = np.ones((Npts,1))/float(Npts)

    mu = np.zeros((Nclasses,Ndims))
    sigma = np.zeros((Nclasses,Ndims,Ndims))

    # ==========================
    # calculate μ and sigma
    for i in range(0,Nclasses):
        k = np.where(labels == i)[0]    # finds the value of k where labels matches the current value of i
        wVal = W[k, :]  # gets w pair at posotion k
        xVal = X[k, :]  # gets x pair at posotion k
        mu[i] = sum(xVal)/findKCount(labels, i)  # compute the value of μ[i] as specified in the lab instructions
        # This allows us to further simplify the expression for
        # the covariance matrix at diagonal indices (m, m) and (m, n), m 6 = n
        sigma[i] = np.diag(sum(np.square((xVal) - mu[i]))/findKCount(labels,i))
        # return the created matrix
    # ==========================
    return mu, sigma


# updated version of mlParams which takes weights into account
def mlParams2(X, labels, W):
    assert(X.shape[0]==labels.shape[0])
    Npts,Ndims = np.shape(X)
    classes = np.unique(labels) # fetches all unique elements from labels
    Nclasses = np.size(classes)

    if W is None:
        W = np.ones((Npts,1))/float(Npts)

    mu = np.zeros((Nclasses,Ndims))
    sigma = np.zeros((Nclasses,Ndims,Ndims))

    for i in range(0,Nclasses):
        k = np.where(labels == i)[0]
        wVal = W[k, :]
        xVal = X[k, :]
        mu[i] = sum(xVal*wVal)/sum(wVal)
        sigma[i] = np.diag(sum(np.square((xVal) - mu[i])*wVal)/sum(wVal))
    return mu, sigma

# in:      X - N x d matrix of M data points
#      prior - C x 1 matrix of class priors
#         mu - C x d matrix of class means (mu[i] - class i mean)
#      sigma - C x d x d matrix of class covariances (sigma[i] - class i sigma)
# out:     h - N vector of class predictions for test points
def classifyBayes(X, prior, mu, sigma):

    Npts = X.shape[0]
    Nclasses,Ndims = np.shape(mu)
    logProb = np.zeros((Nclasses, Npts))

    delta = np.zeros((len(X)))

    # ==========================
    for i in range(0, Npts): # for every data point
        tdp = X[i] # tdp = this data point
        for j in range(0, Nclasses): # for every class
            sDet = np.linalg.det(sigma[j]) #sigma determinant for j
            sInv = np.linalg.inv(sigma[j]) # sigma determinant for j
            tdmcm = tdp - mu[j] # tdmcm = this datapoint minus class mean

            # formula 11
            logProb[j][i] = -1/2*np.log(sDet) -1/2* np.dot(np.dot(tdmcm, sInv), np.transpose(tdmcm)) + np.log(prior[j])
    # ==========================


    # one possible way of finding max a-posteriori once
    # you have computed the log posterior
    h = np.argmax(logProb,axis=0)
    return h


# The implemented functions can now be summarized into the `BayesClassifier` class, which we will use later to test the classifier, no need to add anything else here:


# NOTE: no need to touch this
class BayesClassifier(object):
    def __init__(self):
        self.trained = False

    def trainClassifier(self, X, labels, W=None):
        rtn = BayesClassifier()
        rtn.prior = computePrior2(labels, W)
        rtn.mu, rtn.sigma = mlParams2(X, labels, W)
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBayes(X, self.prior, self.mu, self.sigma)


# ## Test the Maximum Likelihood estimates
#
# Call `genBlobs` and `plotGaussian` to verify your estimates.


# test function
weights=[]
for h in range(0,200):
    weights.append([1/200])

weights = np.array(weights)

#X, labels = genBlobs(centers=5)
#mu, sigma = mlParams2(X,labels, weights)

#classifyBayes(X, prior, mu, sigma)

#test = computePrior(labels) #test function call
#plotGaussian(X,labels,mu,sigma)
#prior = computePrior(labels)

# Call the `testClassifier` and `plotBoundary` functions for this part.
#testClassifier(BayesClassifier(), dataset='wine', split=0.7)
#plotBoundary(BayesClassifier(), dataset='wine',split=0.7)





# ## Boosting functions to implement
#
# The lab descriptions state what each function should do.

# in: base_classifier - a classifier of the type that we will boost, e.g. BayesClassifier
#                   X - N x d matrix of N data points
#              labels - N vector of class labels
#                   T - number of boosting iterations
# out:    classifiers - (maximum) length T Python list of trained classifiers
#              alphas - (maximum) length T Python list of vote weights
def trainBoost(base_classifier, X, labels, T=10):
    # these will come in handy later on
    Npts,Ndims = np.shape(X)

    classifiers = [] # append new classifiers to this list
    alphas = [] # append the vote weight of the classifiers to this list

    # The weights for the first iteration
    wCur = np.ones((Npts,1))/float(Npts)

    for i_iter in range(0, T):
        # a new classifier can be trained like this, given the current weights
        classifiers.append(base_classifier.trainClassifier(X, labels, wCur))

        # do classification for each point
        vote = classifiers[-1].classify(X)

        delta = np.reshape((vote == labels), (Npts,1))

        avoidDivisionByZero = 1e-25

        error = np.sum(wCur * (1 - delta)) + avoidDivisionByZero

        alpha = (np.log(1-error)-np.log(error)) * 0.5

        #Z = np.full(Npts, sum(wCur))

        alphaSign = (delta-.5)/(-.5)
        wCur = wCur * (np.exp(alphaSign*alpha))
        Z = np.sum(wCur)
        #Z = np.full(Npts, sum(wCur))
        wCur /= Z
        alphas.append(alpha) # you will need to append the new alpha

    #print ("classifiers ", classifiers)
    #print ("\n \n alphas ",alphas)
    return classifiers, alphas

# in:       X - N x d matrix of N data points
# classifiers - (maximum) length T Python list of trained classifiers as above
#      alphas - (maximum) length T Python list of vote weights
#    Nclasses - the number of different classes
# out:  yPred - N vector of class predictions for test points
def classifyBoost(X, classifiers, alphas, Nclasses):
    Npts = X.shape[0]
    Ncomps = len(classifiers)

    # if we only have one classifier, we may just classify directly
    if Ncomps == 1:
        return classifiers[0].classify(X)
    else:
        votes = np.zeros((Npts,Nclasses))

        for t in range(0,Ncomps):
            classified = classifiers[t].classify(X)
            for i in range(0,Npts):
                votes[i][classified[i]] += alphas[t]
        return np.argmax(votes,axis=1)
# The implemented functions can now be summarized another classifer, the `BoostClassifier` class. This class enables boosting different types of classifiers by initializing it with the `base_classifier` argument. No need to add anything here.


# NOTE: no need to touch this
class BoostClassifier(object):
    def __init__(self, base_classifier, T=10):
        self.base_classifier = base_classifier
        self.T = T
        self.trained = False

    def trainClassifier(self, X, labels):
        rtn = BoostClassifier(self.base_classifier, self.T)
        rtn.nbr_classes = np.size(np.unique(labels))
        rtn.classifiers, rtn.alphas = trainBoost(self.base_classifier, X, labels, self.T)
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBoost(X, self.classifiers, self.alphas, self.nbr_classes)


# ## Run some experiments
#
# Call the `testClassifier` and `plotBoundary` functions for this part.

#print ("\nBayesClassifier - Iris ")
#testClassifier(BayesClassifier(), dataset='iris', split=0.7)
#plotBoundary(BayesClassifier(), dataset='iris',split=0.7)


#print ("\n \nBayesClassifier - Vowels")
#testClassifier(BayesClassifier(), dataset='vowel', split=0.7)
#plotBoundary(BayesClassifier(), dataset='vowel', split=0.7)


#print ("\n \nBoostClassifier - Iris")
testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset='iris',split=0.7)
#plotBoundary(BoostClassifier(BayesClassifier(), T=10), dataset='iris', split=0.7)



#print ("\n \nBoostClassifier - Vowels")
testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset='vowel',split=0.7)
#plotBoundary(BoostClassifier(BayesClassifier(), T=10), dataset='vowel', split=0.7)



#plotBoundary(BoostClassifier(BayesClassifier()), dataset='iris',split=0.7)


# Now repeat the steps with a decision tree classifier.

#print ("\nIris decision tree classifier")
#testClassifier(DecisionTreeClassifier(), dataset='iris', split=0.7)
#plotBoundary(DecisionTreeClassifier(), dataset='iris',split=0.7)

#print ("\n \nIris decision tree classifier - boost classifier")
#testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='iris',split=0.7)
#plotBoundary(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='iris',split=0.7)


#print ("\n \nVowel decision tree classifier")
#testClassifier(DecisionTreeClassifier(), dataset='vowel',split=0.7)
#plotBoundary(DecisionTreeClassifier(), dataset='vowel',split=0.7)

#print ("\n \nVowel decision tree classifier - boost classifier")
#testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='vowel',split=0.7)
#plotBoundary(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='vowel',split=0.7)



'''




# ## Bonus: Visualize faces classified using boosted decision trees
#
# Note that this part of the assignment is completely voluntary! First, let's check how a boosted decision tree classifier performs on the olivetti data. Note that we need to reduce the dimension a bit using PCA, as the original dimension of the image vectors is `64 x 64 = 4096` elements.


#testClassifier(BayesClassifier(), dataset='olivetti',split=0.7, dim=20)



#testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='olivetti',split=0.7, dim=20)


# You should get an accuracy around 70%. If you wish, you can compare this with using pure decision trees or a boosted bayes classifier. Not too bad, now let's try and classify a face as belonging to one of 40 persons!


#X,y,pcadim = fetchDataset('olivetti') # fetch the olivetti data
#xTr,yTr,xTe,yTe,trIdx,teIdx = trteSplitEven(X,y,0.7) # split into training and testing
#pca = decomposition.PCA(n_components=20) # use PCA to reduce the dimension to 20
#pca.fit(xTr) # use training data to fit the transform
#xTrpca = pca.transform(xTr) # apply on training data
#xTepca = pca.transform(xTe) # apply on test data
# use our pre-defined decision tree classifier together with the implemented
# boosting to classify data points in the training data
#classifier = BoostClassifier(DecisionTreeClassifier(), T=10).trainClassifier(xTrpca, yTr)
#yPr = classifier.classify(xTepca)
# choose a test point to visualize
#testind = random.randint(0, xTe.shape[0]-1)
# visualize the test point together with the training points used to train
# the class that the test point was classified to belong to
#visualizeOlivettiVectors(xTr[yTr == yPr[testind],:], xTe[testind,:])
'''
