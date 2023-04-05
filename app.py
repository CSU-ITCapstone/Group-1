from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
#Create database link here

#Functions for filter_tasks() function
def get_status_count():
    return{
        'not_started' : mongo.db.tasks.count_documents({'status' : 'Not Started'}),
        'in_progress' : mongo.db.tasks.count_documents({'status' : 'In Progress'}),
        'completed' : mongo.db.tasks.count_documents({'status' : 'Completed'}),
    }

def get_priority_count():
    return{
        'low' : mongo.db.tasks.count_documents({'priority' : 'Low'}),
        'medium' : mongo.db.tasks.count_documents({'priority' : 'Medium'}),
        'high' : mongo.db.tasks.count_documents({'priority' : 'High'}),
    }

@app.route('/filter_tasks', methods = ['POST'])
def filter_tasks():
    status_filter = request.form.get('status_filter')
    priority_filter = request.form.get('priority_filter')
    search_filter = request.form.get('search_filter')

    query = {}
    if status_filter:
        query['status'] = status_filter
    elif priority_filter:
        query['priority'] = priority_filter
    elif search_filter:
        query['$text'] = {'$search' : search_filter}
    
    #Find all tasks from the mongoDB table using the value assigned to the query variable
    tasks = mongo.db.tasks.find(query)
    status_count = get_status_count()
    priority_count = get_priority_count()
    total_tasks = mongo.db.tasks.count_documents({})

    return render_template('index.html', tasks=tasks, status_count=status_count, priority_count=priority_count, total_tasks=total_tasks)

if __name__ == '__main__':
    app.run(debug = True)
