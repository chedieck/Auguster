# Auguster

```
usage: auguster.py [-h] [-gp] [-t TRAIN_MODEL] [-l LOOKBACK] [-m MODEL]

Augusto dos Anjos generator. Uses LSTM's,

optional arguments:
  -h, --help            show this help message and exit
  -gp, --generate-poem  generates a random poem
  -t TRAIN_MODEL, --train-model TRAIN_MODEL
                        trains a new <model>.h5, requires --lookback
  -l LOOKBACK, --lookback LOOKBACK
                        lookback to be used on model training or prediction, default
                        is 80
  -m MODEL, --model MODEL
                        <model>.h5 to be used on prediciton, defaults to default
```
