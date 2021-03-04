# Node 5002

from Blockchain import Blockchain

from uuid import uuid4
from flask import Flask, jsonify, request

# Web app
app = Flask(__name__)

# Make an address for this node
nodeAddress = str(uuid4()).replace('-','')

blockchain = Blockchain()

# Mine a new block
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    blockchain.addTransaction(sender = nodeAddress, recipient="Me ho", amount=1)
    block = blockchain.createBlock(proof, previousHash)
    
    response = {'message': "You just mined a block!",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previousHash': block['previousHash'],
                'transactions': block['transactions']}
    
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

# Add a transaction to the blockchain
@app.route('/addTransaction', methods=['POST'])
def addTransaction():
    json = request.get_json()
    transactionKeys = ['sender', 'recipient', 'amount']
    # Check to make sure all keys are there
    if not all (key in json for key in transactionKeys):
        return "Some elements of the transaction are missing", 400
    index = blockchain.addTransaction(json['sender'], json['recipient'], json['amount'])
    response = {'mesasge': f"This transaction will be added to block {index}"}
    return jsonify(response), 201

# Decentralize the chain

# Connect a new node
@app.route('/connectNode', methods=['POST'])
def connectNode():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if nodes is None:
        return "No nodes", 401
    
    for node in nodes:
        blockchain.addNode(node)
        
    response = {'message': "All nodes are now connected. JKC Blockchain now contains: ",
                'totalNodes': list(blockchain.nodes)}
    
    return jsonify(response), 201

# Replace the chain by the longest chain
@app.route('/replaceChain', methods=['GET'])
def replaceChain():
    isChainReplaced = blockchain.replaceChain()
    if (isChainReplaced):
        response = {'message': "The node had a different chain, so the chain was replaced",
                    'newChain': blockchain.chain}
    else:
        response = {'message': "This chain is the largest one",
                    'actualChain': blockchain.chain} 
    return jsonify(response), 200

# Run the program
app.run(host = '0.0.0.0', port = 5002) 

