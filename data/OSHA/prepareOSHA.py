import re
from sklearn.model_selection import train_test_split
from collections import Counter

words = ['hospital', 'hospitalize', 'hospitalized',
               'employer', 'employee', 
               'electric', 'electrical', 'electrocute', 'electrocuted', 'electrocution',
               'approximately', 'approximate',
               'falling', 'fell',
               'trauma', 'traumatic',
               'coworker', 'worker', 'work', 'working',
               'construction',
               'investigation', 'investigate', 'investigating',
               'transport', 'transported', 'transporting',
               'died', 'dead', 'death', 'killed', 'killing',
               'treated', 'treating', 'treatment',
               'operate', 'operating', 'operator', 'operation',
               'caught', ' struck',
               'emergency', 'unguarded',
               'manufacture', 'manufactured', 'manufacturing',
               'however', 'material', 'center', 'symptom',
               'without', 'between',
               'commercial', 'residential', 'company',
               'resulting', 'result', 'exist', 'existing', 
               'pressure', 'unprotected', 'protection',
               'excavator', 'excavating', 'excavation', 'excavate',
               'consist', 'consisting', 'consisted',
               'demolition', 'extent', 'admitted', 'unspecified',
               'fracture', 'removed', 'released', 
                'injuries', 'fatal',
                'crushing', 'crushed', 'excavating', 'excavation',
                'amputate', 'amputated', 'amputation', 
                'power', 'regained', 'unconscious', 'conscious', 
                'transfer', 'transfered', 'transfering',
                'vehicle', 'tractor', 'machine', 
                'height', 'slipped', 'slipping', 'slippery',
                'thumb', 'consciousness', 'lacerated']

def vari(s):
    s = s
    chars = [char for char in s]
    var_chars_lists = []

    for i, char in enumerate(chars[:-1]):
        ls = chars.copy()
        ls[i] = char+' '
        var_chars_lists.append(ls)
    
    return [''.join(list_) for list_ in var_chars_lists]

def replace_words(text, words):
    for word in words:
        vars = vari(word)
        for var in vars:
            text = text.replace(var, word)
    return text

def create_dict(labels):
    label_dict = {}
    for i, label in enumerate(labels):
        label_dict[label] = i
    return label_dict

def load_osha(dataset):
    # load training data
    with open("train.txt", "r", encoding="utf-8") as f:
        raw_train = [line.strip() for line in f]
    list_of_words = [line.split() for line in raw_train]
    # first element is the label
    train_text = [" ".join(line[1:]) for line in list_of_words]
    train_labels = [line[0] for line in list_of_words]
    # load test data
    with open("test.txt", "r", encoding="utf-8") as f:
        raw_test = [line.strip() for line in f]
    list_of_words = [line.split() for line in raw_test]
    # first element is the label
    test_text = [" ".join(line[1:]) for line in list_of_words]
    test_labels = [line[0] for line in list_of_words]
    # create label dictionary
    label_dict = create_dict(set.union(set(train_labels), set(test_labels)))
    # add to dataset
    dataset["train"] = (train_text, train_labels)
    dataset["test"] = (test_text, test_labels)
    dataset["label_dict"] = label_dict
    return dataset

def main():
    with open('raw_data.txt') as f:
        lines = f.read()

    new_text = re.sub('[^ \n\tA-Za-z/_-]+', '', lines)
    new_text = re.sub('[/-]', ' ', new_text)
    new_text = new_text.lower()
    new_text = replace_words(new_text, words)
    
    all_data = new_text.split('\n')

    train_data, test_data= train_test_split(all_data, test_size=0.20, random_state=2022)

    print('\ntotal train:', len(train_data))
    print('\ntotal test:',len(test_data),'\n')

    f1 = open('train.txt','w')
    for item in train_data:
        f1.write(item+'\n')
    f1.close()

    f2 = open('test.txt','w')
    for item in test_data:
        f2.write(item+'\n')
    f2.close()

    d = load_osha({})

    count_train = Counter(d['train'][1])
    count_test = Counter(d['test'][1])

    print('num of training data points per class\n', sorted(count_train.items()))
    print('\nnum of testing data points per class\n', sorted(count_test.items()))

if __name__ == '__main__':
    main()




