from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
#Create database link here
app.config["MONGO_URI"] = "mongodb+srv://muralidharsrihari:databasepasswd@taskdatabase.hdkcea3.mongodb.net/task_manager?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db
db.tasks.create_index([("title", "text"), ("description", "text")]) # Add this line to create a text index on title and description fields
collections = db.list_collection_names()
#Functions for filter_tasks() function
def get_status_counts():
    return{
        'not_started' : mongo.db.tasks.count_documents({'status' : 'Not Started'}),
        'in_progress' : mongo.db.tasks.count_documents({'status' : 'In Progress'}),
        "completed": mongo.db.tasks.count_documents({"status": "Completed"}),
    }

def get_priority_counts():
    return{
        'low' : mongo.db.tasks.count_documents({'priority' : 'Low'}),
        'medium' : mongo.db.tasks.count_documents({'priority' : 'Medium'}),
        'high' : mongo.db.tasks.count_documents({'priority' : 'High'}),
    }
@app.route('/')    
def index():
    tasks = db.tasks.find().sort("priority", -1)
   # print ("tasks = ",tasks)
    status_counts = {
        "not_started": mongo.db.tasks.count_documents({"status": "Not Started"}),
        "in_progress": mongo.db.tasks.count_documents({"status": "In Progress"}),
        "completed": mongo.db.tasks.count_documents({"status": "Completed"})
    }
    priority_counts = {
        "high": mongo.db.tasks.count_documents({"priority": "High"}),
        "medium": mongo.db.tasks.count_documents({"priority": "Medium"}),
        "low": mongo.db.tasks.count_documents({"priority": "Low"})
    }
    total_tasks = db.tasks.count_documents({})
    return render_template('index.html', tasks=tasks, status_counts=status_counts, priority_counts=priority_counts, total_tasks=total_tasks)


@app.route('/add_task', methods= {'POST'})
def add_task():
    task = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "status": request.form.get("status")        
    }
    mongo.db.tasks.insert_one(task)
    return redirect(url_for('index'))

@app.route('/filter_tasks', methods = ['POST'])
def filter_tasks():
    status_filter = request.form.get('status_filter')
    priority_filter = request.form.get('priority_filter')
    search_filter = request.form.get('search_filter')

    query = {}
    if status_filter and priority_filter:
        query['$and'] = [{'status': status_filter}, {'priority': priority_filter}]
    elif status_filter:
        query['status'] = status_filter
    elif priority_filter:
        query['priority'] = priority_filter
    elif search_filter:
        query['$text'] = {'$search' : search_filter}
    
    #Find all tasks from the mongoDB table using the value assigned to the query variable
    tasks = mongo.db.tasks.find(query)
    status_counts = get_status_counts()
    priority_counts = get_priority_counts()
    total_tasks = mongo.db.tasks.count_documents({})

    return render_template('index.html', tasks=tasks, status_counts=status_counts, priority_counts=priority_counts,total_tasks=total_tasks)

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    # Use the ObjectId() function from bson.objectid to convert the task_id string into a MongoDB ObjectId
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    if not ObjectId.is_valid(task_id):
        return redirect(url_for('index'))
    updated_task = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "status": request.form.get("status")
    }
    total_tasks = db.tasks.count_documents({})
    mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": updated_task})
    return redirect(url_for('index'))

        
if __name__ == '__main__':
    app.run(debug = True)
