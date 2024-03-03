import sqlite3

def initialize_database():
    connection = sqlite3.connect('car_inspection.db')
    c = connection.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    status INTEGER DEFAULT 0
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS criteria (
                    id INTEGER PRIMARY KEY,
                    car_id INTEGER,
                    criteria_name TEXT,
                    is_good INTEGER,
                    note TEXT,
                    FOREIGN KEY (car_id) REFERENCES cars(id)
                )''')

    car_list = [
        ("Toyota Camry", 0),
        ("Honda Civic", 0),
        ("Ford Mustang", 0),
        ("Chevrolet Silverado", 0),
        ("BMW 3 Series", 0),
        ("Audi A4", 0),
        ("Mercedes-Benz C-Class", 0),
        ("Tesla Model 3", 0),
        ("Hyundai Elantra", 0),
        ("Kia Forte", 0),
        ("Subaru Outback", 0),
        ("Mazda CX-5", 0),
        ("Nissan Altima", 0),
        ("Volvo XC90", 0),
        ("Volkswagen Jetta", 0),
        ("Jeep Wrangler", 0),
        ("Porsche 911", 0),
        ("Lexus RX", 0),
        ("Infiniti Q50", 0),
        ("Cadillac Escalade", 0)
    ]
    
    # Throw and handle exception where car name is an empty string, None, or contains only whitespace
    try:
        for car in car_list:
            if car[0] is None or not car[0].strip():  
                raise ValueError("Empty name detected for a car.")
    except ValueError as e:
        print("Error:", e)
        connection.close()
        return

    # Handle exception where one or more cars have the same name.
    try:
        c.executemany("INSERT INTO cars (name, status) VALUES (?, ?)", car_list)
    except sqlite3.IntegrityError:
        print("Error: One or more cars have the same name.")
        connection.rollback()
        connection.close()
        return
    
    criteria = [
        "Engine performance",
        "Braking system",
        "Suspension",
        "Interior condition",
        "Exterior condition",
    ]

    # Insert criteria into the database for each car
    for car_id in range(0, len(car_list)):
        for criteria_name in criteria:
            c.execute("INSERT INTO criteria (car_id, criteria_name, is_good, note) VALUES (?, ?, ?, ?)",
                    (car_id, criteria_name, 0, None))

    connection.commit()
    connection.close()

# Function to print all cars and their criteria
def print_all_cars_and_criteria():
    connection = sqlite3.connect('car_inspection.db')
    c = connection.cursor()

    c.execute("SELECT id, name FROM cars")
    cars = c.fetchall()

    for car in cars:
        print(f"{car[1]}:") # Prints car name
        c.execute('''SELECT criteria_name, is_good, note FROM criteria
                     WHERE car_id = ?''', (car[0],)) # Gets criteria with matching car id
        criteria = c.fetchall()
        for crit in criteria:
            print(f"    {crit[0]} - Is good: {bool(crit[1])}, Note: {crit[2] if crit[2] else 'No note'}")
            # Prints criteria with Is_good and note field

    connection.close()

# Main function
if __name__ == "__main__":
    #initialize_database()
    print_all_cars_and_criteria() 
