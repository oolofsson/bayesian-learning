# bayesian-learning
# Machine Learning Lab

### Questions to answer:
#### 1. When can a feature independence assumption be reasonable and when not?

* A reasonable assumption of an independent feature would be when the feature is not related to anything else. For example a persons height is not related to whether the person is right or left handed.
* A non reasonable feature independence assumption would be when assuming that something is independent when in fact there are no occurrences between the class label and a feature. This leads to a likelihood of 0. And is thus not a reasonable assumption of independence, as there is no data to back it back up.

#### 2. How does the decision boundary look for the Iris dataset? How could one improve the classification results for this scenario by changing classifier or, alternatively, manipulating the data?

* Boosting should have a positive effect on the classification results.

* Different points may have different importance when it comes to deciding the boundary. It could be possible to change the weights of these points so that they may or may not effect the boundary in a different way.
