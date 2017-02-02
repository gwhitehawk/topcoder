# Topcoder problem:
# The goal is to generate a sequence of integers of a given length,
# where each element is coprime ONLY with its immediate neighbors/
# Usage:
# python coprime_neighbors.py [sequence_length]


import sys


class NDiv(object):
    def __init__(self, value, primes):
        self.value = value
        self.primes = primes


def gen_primes():
    divisors = {}

    q = 2

    while True:
        if q not in divisors:
            yield q
            divisors[q * q] = [q]
        else:
            for p in divisors[q]:
                divisors.setdefault(p + q, []).append(p)
            del divisors[q]

        q += 1

def find_sequence(seq_len):
    """
      The idea is as follows:
      To generate the n-th element, we know:
      - It's coprime to (n-1)th
      - The (n-2)th element has a common divisor with all elems 1 .. (n-4).

      We hence calculate x_n = x_{n-2} * p, where
      a) p is a prime dividing x_{n-3} but not x_{n-1} if such prime exists
      b) p is a not yet used prime, and in this case, we overwrite: x_{n-3} := x_{n-3} * p
      The second assignment guarantees that x_{n-3} the gcd of x_{n-3} and its neighbors
      remains unchanged, while gcd(x_{n-3}, x_n) = p
    """
    res = [NDiv(2, [2]), NDiv(3, [3]), NDiv(10, [2, 5])]
    prime_gen = gen_primes()
    max_prime = 5
    p = 1
    while p < max_prime:
        p = prime_gen.next()

    while len(res) < seq_len:
        avail_primes = set(res[len(res) - 3].primes) - set(res[len(res) - 1].primes)
        new_prime = -1
        if avail_primes:
            new_prime = sorted(avail_primes)[0]
        else:
            new_prime = prime_gen.next()
            res[len(res) - 3].value *= new_prime
            res[len(res) - 3].primes.append(new_prime)
        new_num = res[len(res) - 2].value * new_prime
        new_primes = res[len(res) - 2].primes + [new_prime]
        res.append(NDiv(new_num, new_primes))
    return res

if __name__ == '__main__':
    seq_len = int(sys.argv[1])

    res = find_sequence(seq_len)
    for i in res:
        print i.value
