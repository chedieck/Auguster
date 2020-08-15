import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, Conv1D, MaxPool1D,\
        Bidirectional, LSTM, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np
import regex as re
import argparse
# hide debugging info


class SaveCallback(Callback):
    def __init__(self, model_name):
        self.model_name = model_name

    def on_epoch_end(self, epoch, logs={}):
        self.model.save(f'Modelos/{self.model_name}.h5')


def generate_windows(sequences, lookback, batch_size=32):
    x = []
    y = []
    for sentence in sequences:
        for p in range(len(sentence) - lookback):
            aux = sentence[p:p + lookback]
            if not aux.any():
                continue
            x.append(aux)
            y.append(sentence[p + lookback])
    ys = to_categorical(y, num_classes=total_words+1)
    return np.array(x), ys


def train(x, y, lookback=80, model_name='default', nunits=40, epochs=200):
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model = Sequential()
    model.add(Embedding(len(tokenizer.word_index)+1, 64,
              input_length=lookback))
    model.add(Conv1D(64, 3))
    model.add(MaxPool1D(2))
    model.add(Conv1D(64, 3))
    model.add(MaxPool1D(2))
    model.add(Bidirectional(LSTM(nunits)))
    model.add(Dense(total_words + 1, activation='softmax'))
    adam = Adam(lr=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=adam,
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(x, y, epochs=epochs,
                        callbacks=[SaveCallback(model_name)])
    return history, model


def frase_encode(string):
    """
    transforma a string em uma lista de tokens
    """
    return [tokenizer.word_index[s] for s in string.split()]


def frase_decode(sequence):
    """
    transforma uma lista de tokens em uma string
    """
    return ' '.join([invdict[s] for s in sequence])


def prever_proximas(startstring, model):
    aux = frase_encode(startstring)
    previsões = []
    pred_word = ''
    while pred_word != '0f0':
        pred = model.predict(np.array([aux]))
        pred_token = np.argmax(pred)
        pred_word = frase_decode([pred_token])  # próxima palavra
        previsões.append(pred_word)
        aux.append(pred_token)
        aux = aux[1:]
    return previsões


def capitalize_verse(match):
    return match.group(0)[:-1] + match.group(1).upper()


def unformat(texto):
    aux = texto.replace('0v0', '\n')
    aux = aux.replace('0e0', '\n\n')
    aux = re.sub(r'\n( +[a-z])', capitalize_verse, aux)
    return aux


def generate_augusto(x, model):
    while 1:
        try:
            random_start = frase_decode(x[np.random.choice(len(x))])
            texto = ' '.join(prever_proximas(random_start, model))
            break
        except KeyError:
            continue
    return unformat(texto)


def init_argparse():
    headline = "Augusto dos Anjos generator. Uses LSTM's, "
    "which are not ideal for data generation"
    parser = argparse.ArgumentParser(description=headline)
    parser.add_argument('-gp', '--generate-poem', action='store_true',
                        help='generates a random poem')
    parser.add_argument('-t', '--train-model',
                        help='trains a new <model>.h5, requires --lookback')
    parser.add_argument('-l', '--lookback', type=int,
                        help='lookback to be used on model training or'
                        ' prediction, default is 80')
    parser.add_argument('-m', '--model',
                        help='<model>.h5 to be used on prediciton,'
                        ' defaults to default')
    args = parser.parse_args()
    if args.train_model and not args.lookback:
        print("lookback not set, setting it to 80")
        args.lookback = 80
    print(args)
    return args


if __name__ == '__main__':
    args = init_argparse()
    tokenizer = Tokenizer()

    with open('DB/poems.txt', 'r') as f:
        sentences = f.readlines()

    tokenizer.fit_on_texts(sentences)
    total_words = len(tokenizer.word_index)
    invdict = {v: k for k, v in tokenizer.word_index.items()}
    sequences = tokenizer.texts_to_sequences(sentences)
    padded = pad_sequences(sequences, padding='post')
    print("Generating windows...")
    x, y = generate_windows(padded, 80)

    if args.generate_poem:
        # use a custom model
        if model_name := args.model:
            pass
        else:
            model_name = 'default'

        print("Loading model...")
        model = load_model(f'Modelos/{model_name}.h5')
        print("Generating poem, this may take a while...")
        print(generate_augusto(x, model))
    if model_name := args.train_model:
        h, m = train(x,y, lookback=args.lookback, model_name=model_name, epochs=10)



    pass
