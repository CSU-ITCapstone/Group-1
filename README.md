# Group-1

#Functions called by a user
#filter_tasks(): Assigns a filter selected by a user to a query variable, then a query of the database table using
#the assigned value occurs. Each task with the selected filter value is counted and displayed on the list, along
#with the number of tasks with each priority and status value, and the total number of tasks with the selected filter

#Functions not directly called by a user
#get_status_count(): Used by filter_tasks() to count the number of tasks with each status value
#get_priority_count(): Used by filter_tasks() to count the number of tasks with each priority value