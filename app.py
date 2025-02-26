from flask import Flask, jsonify
import random
import time
import threading

app = Flask(__name__)

# Sample Agents (Tellers/Call Center Agents)
agents = [
    {"id": 1, "name": "Agent 1", "busy": False, "tasks": 0},
    {"id": 2, "name": "Agent 2", "busy": False, "tasks": 0},
    {"id": 3, "name": "Agent 3", "busy": False, "tasks": 0},
]

# Customer Queue
customers = []

# Scheduling Algorithms
def round_robin():
    for customer in customers:
        for agent in agents:
            if not agent["busy"]:
                assign_task(agent, customer)
                break

def priority_scheduling():
    customers.sort(key=lambda x: x['priority'], reverse=True)  # Higher priority first
    for customer in customers:
        for agent in agents:
            if not agent["busy"]:
                assign_task(agent, customer)
                break

def shortest_job_next():
    customers.sort(key=lambda x: x['service_time'])  # Shortest task first
    for customer in customers:
        for agent in agents:
            if not agent["busy"]:
                assign_task(agent, customer)
                break

def assign_task(agent, customer):
    agent["busy"] = True
    agent["tasks"] += 1
    customers.remove(customer)
    threading.Thread(target=complete_task, args=(agent, customer)).start()

def complete_task(agent, customer):
    time.sleep(customer["service_time"])  # Simulating processing time
    agent["busy"] = False

# API Endpoints
@app.route("/assign", methods=["GET"])
def assign():
    round_robin()  # You can change this to priority_scheduling() or shortest_job_next()
    return jsonify({"message": "Tasks Assigned!", "agents": agents})

@app.route("/add_customer", methods=["POST"])
def add_customer():
    customer = {
        "id": len(customers) + 1,
        "priority": random.choice([1, 2, 3]),  # 1: Normal, 2: Corporate, 3: VIP
        "service_time": random.randint(2, 5)  # Time required for service
    }
    customers.append(customer)
    return jsonify({"message": "Customer Added!", "customer": customer})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"agents": agents, "customers": customers})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
