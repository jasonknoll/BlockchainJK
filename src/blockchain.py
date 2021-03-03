# Create a simple blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building

class Block:
    pass

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash='0') # Geneis block
        
    def createBlock(self, proof, previousHash):
        # Basic foundations of a block (for crypto)
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash}
        
        self.chain.append(block)
        return block
    
    def getPreviousBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, previousProof):
        newProof = 1 # Initialize to 1. Will increment, until right proof is calculated
        checkProof = False
        
        while (checkProof != True):
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest() # Very simple operation
            
            # Check for leading zeroes
            if (hashOperation[:4] == '0000'):
                checkProof = True
            else:
                newProof += 1      
        return newProof

    def hash(self, block):
        # Block must be in correct format
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    # Verify blocks using the hash values
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1 # first block
        
        while (blockIndex < len(chain)):
            block = chain[blockIndex] # Current block
            if (block['previousHash'] != self.hash(previousBlock)):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            
            if (hashOperation[:4] != '0000'):
                return False
            
            previousBlock = block
            blockIndex += 1
        return True
 
#---------------------------------
       
# Part 2 - Mining (Using flask)

app = Flask(__name__)
blockchain = Blockchain()

# Mine a new block
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    
    response = {'message': "You just mined a block!",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previousHash': block['previousHash']}
    
    return jsonify(response), 200 # http status code

# Get the full blockchain
@app.route('/getChain', methods=['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

@app.route('/isValid', methods=['GET'])
def isValid():
    if (blockchain.isChainValid(blockchain.chain)):
        response = {'message': "The chain is valid!"}
    else:
        response = {'message': "The blockchain is not valid!"} # Obviously would need to be more specific
    return jsonify(response), 200

# Run the program
app.run(host = '0.0.0.0', port = 5000) 