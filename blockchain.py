from datetime import datetime
import hashblock


class Blockchain:
    def __init__(self, leading=4):
        self.chain = []
        self.create_block(proof=1, prev_hash='0', data='Mustafa has 200$')
        self.leading = leading

    def create_block(self, proof, prev_hash, data):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'prev_hash': prev_hash,
            'data': data
        }
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        length = len(self.chain)
        prev_block = self.chain[0]
        block_index = 1
        while block_index < length:
            block = self.chain[block_index]
            if block['prev_hash'] != hashblock.hash_block(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashblock.hash_proof(proof, prev_proof)
            if hash_operation[:self.leading] != ''.zfill(self.leading):
                return False
            prev_block = block
            block_index += 1
        return True
