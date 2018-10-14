# bayesian-learning
# Machine Learning Lab

### Questions to answer:
#### 1. When can a feature independence assumption be reasonable and when not?

* A reasonable assumption of an independent feature would be when the feature is not related to anything else. For example a persons height is not related to whether the person is right or left handed.
* A non reasonable independence assumption would be to assume that things that are clearly influenced by each other are independent. For example a person's weight and height.

#### 2. How does the decision boundary look for the Iris dataset? How could one improve the classification results for this scenario by changing classifier or, alternatively, manipulating the data?

* Boosting should have a positive effect on the classification results.

* Different points may have different importance when it comes to deciding the boundary. It could be possible to change the weights of these points so that they may or may not effect the boundary in a different way.

#### 3. 
(1) Is there any improvement in classification accuracy? Why/why not?  

(2) Plot the decision boundary of the boosted classifier on iris and compare it with
that of the basic. What differences do you notice? Is the boundary of the boosted
version more complex?  

(3) Can we make up for not using a more advanced model in the basic classifier
(e.g. independent features) by using boosting?  



#### 4. If you had to pick a classifier, naive Bayes or a decision tree or the boosted versions of these, which one would you pick? Motivate from the following criteria:

* Outliers  
Bayes without boosting, boosting will tend to focus on the outliers and screw up the classifier.
* Irrelevant inputs: part of the feature space is irrelevant  
Decision Trees with boosting, will focus on adding as much information gain as possible and not care about irrelevant inputs.
* Predictive power  
Naive Bayes with boosting, naive bayes will build distributions which makes better predictions.
* Mixed types of data: binary, categorical or continuous features, etc.  
Naive Bayes can adapt the maximum likelihood estimation based on the distribution and thus probably perform better, boosting will make it even better since it will compare the performance of these distributions.
* Scalability: the dimension of the data, D, is large or the number of instances, N, is large, or both.  
Decision Trees will perform better on large datasets.
