from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Get cars from the database (id, name, status)
def get_cars():
    try:
        connection = sqlite3.connect('car_inspection.db')
        c = connection.cursor()
        c.execute("SELECT * FROM cars")
        cars = c.fetchall()
        return cars
    except sqlite3.Error as e:
        print("Error fetching cars:", e)
        return []

# Get criteria for a specific car (criteria_name, is_good, note)
def get_criteria(car_id):
    try:
        connection = sqlite3.connect('car_inspection.db')
        c = connection.cursor()
        c.execute("SELECT criteria_name, is_good, note FROM criteria WHERE car_id=?", (car_id,))
        criteria = c.fetchall()
        return criteria
    except sqlite3.Error as e:
        print("Error fetching criteria:", e)
        return []

# Route for the home page which displays list of cars
@app.route('/')
def index():
    cars = get_cars()
    return render_template('index.html', cars=cars)

# Route for the inspection results page for each car which displays list of criteria
@app.route('/inspection_results/<int:car_id>', methods=['GET', 'POST'])
def inspection_results(car_id):
    try:
        # When criteria form is saved, update the database with the values.  
        if request.method == 'POST':
            data = request.form
            connection = sqlite3.connect('car_inspection.db')
            c = connection.cursor()
            criteria_met = 0  # Counter to track the number of criteria met
    
            criteria = get_criteria(car_id)
            criteria_names = [field[0] for field in criteria]
            
            # Update is_good field in criteria based on form data
            for criteria_name in criteria_names:
                is_good = 1 if data.get(criteria_name) == 'on' else 0
                c.execute("UPDATE criteria SET is_good=? WHERE car_id=? AND criteria_name=?", (is_good, car_id, criteria_name))
                if is_good:
                    criteria_met += 1
                    
                # Get the total number of criteria for the car
                total_criteria = len(criteria)
                
                if criteria_met == total_criteria:
                    car_status = 2  # All criteria met
                elif criteria_met > 0:
                    car_status = 1  # Some criteria met
                else:
                    car_status = 0  # No criteria met
                    
                # Update the status of the car in the database
                c.execute("UPDATE cars SET status=? WHERE id=?", (car_status, car_id))

            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        else:
            criteria = get_criteria(car_id)
            return render_template('inspection_results.html', criteria=criteria)
    except sqlite3.Error as e:
        print("Database error occurred:", e)
        return render_template('error.html', error_message="Database error occurred: " + str(e))
    except Exception as e:
        print("An error occurred:", e)
        return render_template('error.html', error_message="An error occurred: " + str(e))

# When note is saved, update the notes field of criteria in database with text input
@app.route('/save_note', methods=['POST'])
def save_note():
    try:
        data = request.json
        criteria_name = data.get('criteria_name')
        note = data.get('note')

        connection = sqlite3.connect('car_inspection.db')
        c = connection.cursor()
        c.execute("UPDATE criteria SET note=? WHERE criteria_name=?", (note, criteria_name))
        connection.commit()
        connection.close()

        return jsonify({'message': 'Note saved successfully.'})
    except sqlite3.Error as e:
        print("Database error occurred:", e)
        return jsonify({'error': 'Database error occurred: ' + str(e)})
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': 'An error occurred: ' + str(e)})

if __name__ == '__main__':
    app.run()