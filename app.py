from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    todo_list = request.form.getlist('todo_list')
    time_spent_dict = {}

    for task in todo_list:
        time_spent = int(request.form[task])
        time_spent_dict[task] = time_spent

    visualize_day(todo_list, time_spent_dict)
    save_data(todo_list, time_spent_dict)

    return render_template('success.html')

def visualize_day(todo_list, time_spent_dict):
    labels = todo_list
    sizes = [time_spent_dict[label] for label in labels]
    colors = plt.cm.Paired(range(len(labels)))

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    plt.savefig('static/pie_chart.png')
    plt.close()

def save_data(todo_list, time_spent_dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"day_summary_{timestamp}.txt"

    with open(filename, 'w') as file:
        file.write("Day Summary - {}\n\n".format(timestamp))
        file.write("To-Do List:\n")
        for task in todo_list:
            file.write("- {}\n".format(task))

        file.write("\nTime Spent:\n")
        for task, time_spent in time_spent_dict.items():
            file.write("- {}: {} minutes\n".format(task, time_spent))

    print("Data saved to '{}'.".format(filename))

if __name__ == '__main__':
    app.run(debug=True)
