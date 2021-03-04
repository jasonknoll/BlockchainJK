# Create a simple blockchain

import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse

# Part 1 - Building

class Block:
    pass

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = [] # Containing all transactions before they're added to a block
        self.createBlock(proof=1, previousHash='0') # Geneis block
        self.nodes = set()
        
    def createBlock(self, proof, previousHash):
        # Basic foundations of a block (for crypto)
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash,
                 'transactions': self.transactions}
        
        self.transactions = [] # Empty the list after it's added to block
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
                #print(str(hashOperation))
            else:
                newProof += 1
                #print(newProof)
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
    
    def addTransaction(self, sender, recipient, amount):
        self.transactions.append({'sender': sender,
                                  'recipient': recipient,
                                  'amount': amount})
        previousBlock = self.getPreviousBlock()
        return previousBlock['index'] + 1 # Returns the block index for this transaction
    
    def addNode(self, address):
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)
        
    def replaceChain(self):
        network = self.nodes
        longestChain = None
        maxLength = len(self.chain) 
        
        for node in network:
            print(node)
            response = requests.get(f"http://{node}/getChain")
            print("pls")
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > maxLength and self.isChainValid(chain):
                    maxLength = length
                    longestChain = chain
        if longestChain:
            self.chain = longestChain
            return True
        return False
        