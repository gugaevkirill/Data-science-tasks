import re
from typing import List, Tuple

import numpy as np
import scipy.spatial as sp


class Cosinusator:
    def process(self, filename_in: str, filename_out: str):
        sentence_tokens, strings = self.get_sentence_tokens(filename_in)
        augmented_matrix = self.get_matrix(sentence_tokens)

        needle = augmented_matrix[0]
        matrix = augmented_matrix[1:]
        indexes = self.get_closest_indexes(needle, matrix, 2)

        self.write_output(indexes, filename_out)

    @staticmethod
    def get_sentence_tokens(filename: str) -> Tuple[List[List[str]], List[str]]:
        file = open(filename, 'r')
        strings = file.readlines()
        tokens = [re.split('[^a-z]', string.lower()) for string in strings]
        file.close()
        return [list(filter(None, t)) for t in tokens], strings

    @staticmethod
    def get_all_tokens(sentence_tokens: List[List[str]]) -> List[str]:
        flatten = [s for sentence in sentence_tokens for s in sentence]
        flatten = list(set(flatten))
        print("Total tokens: %s" % len(flatten))
        return flatten

    @staticmethod
    def get_matrix(sentence_tokens: List[List[str]]) -> List[List[int]]:
        token_list = Cosinusator.get_all_tokens(sentence_tokens)

        matrix = []
        for sentence in sentence_tokens:
            tmp = [sentence.count(token) for token in token_list]
            matrix.append(tmp)

        return matrix

    @staticmethod
    def get_closest_indexes(needle: List[int], matrix: List[List[int]], count: int) -> List[int]:
        distances = np.array([sp.distance.cosine(needle, hayshake) for hayshake in matrix])

        indexes = []
        for i in range(count):
            index = np.argmin(distances)
            indexes.append(index)
            distances[index] += 1

        return indexes

    @staticmethod
    def write_output(ans: List[int], filename: str) -> None:
        file = open(filename, 'w')
        file.write(' '.join([str(i + 1) for i in ans]))
        file.close()


cos = Cosinusator()
cos.process('sentences.txt', 'submission-1.txt')
