import pathlib
import pickle

import numpy as np
import pandas as pd

from .utils import normalizer


class TextToVec:
    """
    TextToVec modoule
    """
    def __init__(self):
        self.confidence = 2
        self.n_factors = 300
        resources_path = pathlib.Path(__file__).parent / "resources"
        item_factors = pd.read_pickle(resources_path.joinpath("item_factors.pickle").as_posix())
        self.A = np.asarray(item_factors)
        self.inverse_matrix = np.linalg.solve(self.A.T.dot(self.A), self.A.T)
        self.zero_matrix = np.zeros(self.n_factors)
        with open(resources_path.joinpath("item_codes.pickle").as_posix(), "rb") as file:
            item_codes = pickle.load(file)
        item_codes = item_codes.reset_index(drop=True)
        self.item_codes = {
            item_codes["item"][i]: item_codes["item_code"][i] for i in range(len(item_codes))
        }

    def term_finder(self, the_text):
        token_count = 5
        the_text = the_text + " --- --- --- --- --- --- "
        m_array = list(range(token_count))
        tokenized_text = the_text.split()
        aa = []
        for x in range(len(tokenized_text) - 5):
            for j in range(token_count):
                m_array[j] = tokenized_text[x + j]
            token = ""
            for e in range(token_count):
                token = token + " " + m_array[e]
                token = token.strip()
                if token in self.item_codes.keys():
                    aa = [*aa, token]
        return aa

    def term_to_code(self, the_terms):
        return [self.item_codes[x] for x in the_terms]

    def the_text_factor(self, text):
        term_codes = self.term_to_code(self.term_finder(text))
        unique_term_codes = list(set(term_codes))
        unique_term_codes.sort()
        term_codes_dict = {i: term_codes.count(unique_term_codes[i]) for i in range(len(unique_term_codes))}
        inv = self.inverse_matrix[:, unique_term_codes]
        if len(unique_term_codes) == 00:
            return self.zero_matrix
        else:
            aa = 0
            for i in range(len(unique_term_codes)):
                aa += inv[:, i] * term_codes_dict[i]
            return aa

    def call(self, x):
        if not x:
            return self.zero_matrix
        else:
            return normalizer(self.the_text_factor(x))

    def __call__(self, x):
        return self.call(x)
