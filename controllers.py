import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from Blockchain import Blockchain


# load blockchains from database
Blockchain.load_blockchains()

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')



def mine(user):

    blockchain = Blockchain.get_blockchain(user)

    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # No reward for mining :P 

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return response
  


def create_transaction(user, doctor, report, tup):

    blockchain = Blockchain.get_blockchain(user)


    # Create a new Transaction
    index = blockchain.new_transaction(user, doctor, report, tup)

    response = {'message': f'Transaction will be added to Block {index}'}
    return response



def full_chain(user):


    blockchain = Blockchain.get_blockchain(user)

    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return response



def register_nodes(user, nodes):  # WIP

    blockchain = Blockchain.get_blockchain(user)

    if nodes is None:
        return "Error: Please supply a valid list of nodes"

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return response


# resolve node

def consensus(user):  # WIP

    blockchain = Blockchain.get_blockchain(user)

    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

        return response
