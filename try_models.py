import analyze
import glob
import pdb
import nltk
import time


path = analyze.data_path_dev + 'dev-24'
list_of_file = sorted(glob.glob(path))
fl_pairs = []

for file in list_of_file:
    fl_pairs += analyze.analyze_single_file(file)

#list_lemma_form = list(filter(lambda l: l[0].isalpha(), fl_pairs))
list_lemma_form = fl_pairs

list_lemma = [l for l, f in list_lemma_form]

start = time.time()

# POS tag
#list_lemma_tag = nltk.pos_tag(list_lemma)

# Unigram
features_set = [({"lemma": lf[0]}, lf[0] == lf[1]) for lf in list_lemma_form]


#
train_set = features_set[:int(len(features_set)*0.9)]
test_set = features_set[len(train_set):]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, test_set))*100)
print("Time:", time.time() - start)

# # With POS tag
# features_set_pos = [({"lemma": lf[0], "pos": lt[1]}, lf[0] == lf[1]) for lf, lt in zip(list_lemma_form, list_lemma_tag)]
#
# train_set = features_set_pos[:int(len(features_set_pos)*0.9)]
# test_set = features_set_pos[len(train_set):]
#
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print("Classifier accuracy percent (POS):", (nltk.classify.accuracy(classifier, test_set))*100)
# print("Time:", time.time() - start)

# Bigram
features_set_bigram = [({"lemma": lemma, "lemma-1": fl_pairs[index][0]}, lemma == forme) for index, (lemma, forme) in enumerate(fl_pairs[1:])]
train_set = features_set_bigram[:int(len(features_set_bigram)*0.9)]
test_set = features_set_bigram[len(train_set):]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print("Classifier accuracy percent (Bigram):", (nltk.classify.accuracy(classifier, test_set))*100)
print("Time:", time.time() - start)

# Trigram
features_set_trigram = [({"lemma": lemma, "lemma-1": fl_pairs[index][0], "lemma-2": fl_pairs[index-1][0]}, lemma==forme) for index, (lemma, forme) in enumerate(fl_pairs[2:])]
train_set = features_set_trigram[:int(len(features_set_trigram)*0.9)]
test_set = features_set_trigram[len(train_set):]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print("Classifier accuracy percent (Trigram):", (nltk.classify.accuracy(classifier, test_set))*100)
print("Time:", time.time() - start)


end = time.time()
print("Total time in seconds:", end - start)

pdb.set_trace()


# Calculate the accuracy by giving the classes result list.
def cal_accuracy(class_r, test_set):
    correct = 0
    for index,c in enumerate(class_r):
        if c == test_set[index][1]:
            correct += 1
    return correct/len(class_r)

#test_data =
#test_lemma =