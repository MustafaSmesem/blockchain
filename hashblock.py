import hashlib
import json


def proof_of_work(prev_proof, leading=4):
    new_proof = 1
    while True:
        hash_operation = hash_proof(new_proof, prev_proof)
        if hash_operation[:leading] == ''.zfill(leading):
            print(str(new_proof) + ' -> ' + hash_operation)
            return new_proof
        new_proof += 1


def hash_block(block):
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()


def hash_proof(new_proof, prev_proof):
    return hashlib.sha256(str(new_proof ** 2 - prev_proof).encode()).hexdigest()
