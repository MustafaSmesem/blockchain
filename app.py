from flask import Flask, jsonify, request
from blockchain import Blockchain
import hashblock
from datetime import datetime

app = Flask(__name__)
leading = 4
blockchain = Blockchain(leading=leading)


@app.route('/')
def index():
    doc = {
        'blockchain': {
            'get_chain': {
                'method': 'GET',
                'url': '/api/blockchain/get_chain'
            },
            'is_chain_valid': {
                'method': 'GET',
                'url': '/api/blockchain/is_chain_valid'
            },
            'hash_block': {
                'method': 'POST',
                'url': 'api/blockchain/hash_block',
                'body': {
                    "index": "block_index",
                    "prev_hash": "previous_block_hash",
                    "proof": "proof_number",
                    "timestamp": "block_mining_timestamp"
                }
            },
            'mine_block': {
                'method': 'POST',
                'url': 'api/blockchain/mine_block',
                'body': {"data": "block_data"}
            }
        }
    }
    return jsonify(doc)


@app.route('/api/blockchain/get_chain')
def get_chain():
    chain = []
    for block in blockchain.chain:
        current_hash = hashblock.hash_block(block)
        chain.append({
            'block': block,
            'hash': current_hash
        })
    result = {
        'blockchain': chain,
        'is_chain_valid': blockchain.is_chain_valid(),
        'length': len(chain)
    }
    return jsonify(result)


@app.route('/api/blockchain/is_chain_valid')
def is_chain_valid():
    is_valid = blockchain.is_chain_valid()
    message = 'All good, This blockchain is valid' if is_valid else 'Oops, This blockchain is invalid'
    result = {
        'is_chain_valid': is_valid,
        'message': message,
        'timestamp': str(datetime.now())
    }
    return jsonify(result)


@app.route('/api/blockchain/hash_block', methods=['POST'])
def hash_block():
    request_data = request.get_json()
    result = {
        'block': request_data,
        'hash': hashblock.hash_block(request_data)
    }
    return jsonify(result)


@app.route('/api/blockchain/mine_block', methods=['POST'])
def mine_block():
    request_data = request.get_json()
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = hashblock.proof_of_work(prev_proof, leading=leading)
    block = blockchain.create_block(proof, hashblock.hash_block(prev_block), request_data['data'])
    result = {
        'block': block,
        'hash': hashblock.hash_block(block),
        'message': "Congratulation you have just mined a block and it will be added to the block chain"
    }
    return jsonify(result)
