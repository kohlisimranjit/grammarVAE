from __future__ import print_function

import argparse
import os
import h5py
import numpy as np

from models.model_eq import MoleculeVAE
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import pdb
import h5py
import eq_grammar as G

MAX_LEN = 15
LATENT = 25
EPOCHS = 50
BATCH = 600

rules = G.gram.split('\n')
DIM = len(rules)


def get_arguments():
    parser = argparse.ArgumentParser(description='Molecular autoencoder network')
    parser.add_argument('--epochs', type=int, metavar='N', default=EPOCHS,
                        help='Number of epochs to run during training.')
    parser.add_argument('--latent_dim', type=int, metavar='N', default=LATENT,
                        help='Dimensionality of the latent representation.')
    return parser.parse_args()

def main():

    # 0. load dataset
    h5f = h5py.File('data/eq2_grammar_dataset.h5', 'r')
    data = h5f['data'][:]
    h5f.close()

    # 1. get any arguments and define save file, then create the VAE model
    args = get_arguments()
    params = {'hidden': 100, 'dense': 100, 'conv1': 2, 'conv2': 3, 'conv3': 4}
    model_save = 'eq_vae_grammar_h' + str(params['hidden']) + '_c234_L' + str(args.latent_dim) + '_E' + str(args.epochs) + '_batchB.hdf5'
    model = MoleculeVAE()

    # 2. if this results file exists already load it
    model.load(rules, model_save, latent_rep_size = args.latent_dim, hypers = params)
    embeddings = model.encoderMV.predict(data)
    np.save("embedding", embeddings[0])
    
if __name__ == '__main__':
    main()
