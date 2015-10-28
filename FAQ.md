Numenta Anomaly Benchmark FAQ
--------

#### Do I need to optimize the threshold(s) before scoring a DUT?
No, but there needs to be a corresponding entry in /config/thresholds.json for the DUT, where the values are NULL.

#### Why do the NAB scores not correlate with precision, recall, and F1 score?
Precision, recall, and their harmonic mean, F1 score, are helpful evaluation functions for most machine learning algorithms. They don't, however, incorporate time in the calculations, and are thus unsuitable for evaluating the ability of an algorithm to perform on real-time, streaming data. A main motivation for the NAB was to design a scoring system which incorporates time and the TP,TN,FN, and FP counts.

See also: [Precision and Recall](http://en.wikipedia.org/wiki/Precision_and_recall), [F1 Score](http://en.wikipedia.org/wiki/F1_score)


#### The TP, TN, FP, and FN have different values between different profiles. Why?
It is okay for the metrics' counts to for different application profiles. For a given DUT, the optimization step calculates the best threshold -- i.e. likelihood value above which a data point is anomalous -- for each application profile, where the best threshold is that which maximizes the score. Thus, consider the application profile "Rewards Low FP Rate". The optimal threshold for this profile will likely be higher than that of the other profiles because then the DUT outputs fewer detections, which likely results in fewer FPs.

#### What is this error I keep getting with path and/or file names?
NAB steps will recurse through the data and results directories, so keeping any extra files there will cause errors. And folow the naming conventions explicitly!

#### How can I test my own anomaly detection algorithm?
Several options with step-by-step instructions and examples are detailed here in the wiki.

#### I ran the detection step and my results files are different than those checked in. Did I do something wrong?
Try running the scoring and normalization steps, which write additional columns to these files with the scores for each record. This is likely the difference.

