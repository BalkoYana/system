import random
from enum import Enum

class Course:
    def __init__(self, professor, course, subject, typeOfClass, numberOfClassWeek, duration):
        self.professor = professor
        self.course = course
        self.subject = subject
        self.typeOfClass = typeOfClass
        self.number = numberOfClassWeek
        self.duration = duration

    def __str__(self):
        return "Course {} | Professor '{}' | Subject '{}' |  \n" \
          .format(self.course, self.professor, self.subject)

    def __repr__(self):
        return str(self)

class Room:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "{} - {} \n".format(self.name, self.type)

    def __repr__(self):
        return str(self)

class WeekDay(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

class TimetableCustom:
    def __init__(self, name, num_specializations, fixedslots=False):
        self.name = name
        self.num_specializations = num_specializations
        self.final = {day.name.lower(): {i + 1: fixedslots for i in range(4 * num_specializations)} for day in WeekDay if day != WeekDay.SAT and day != WeekDay.SUN}


    def __str__(self):
        timetable_str = ""
        for day, slots in self.final.items():
            timetable_str += f"{day}: {slots}\n"
        return timetable_str

def group_classes_by_specialization(classes):
    specializations = {}
    for class_obj in classes:
        if class_obj.course not in specializations:
            specializations[class_obj.course] = []
        specializations[class_obj.course].append(class_obj)
    return specializations

def load_classes():
    classes = [
        Course("Smith", "CA1", "Programming", "Lecture", 3, 3),
        Course("Smith", "CA1", "Programming", "P", 2, 2),
        Course("Jones", "CA1", "Data Structures", "Lecture", 2, 3),
        Course("Jones", "CA1", "Data Structures", "P", 3, 3),
        Course("Smith", "CA1", "History", "P", 1, 3),
        Course("Smith", "CA1", "History", "Lecture", 1, 3),
        Course("Brown", "CA1", "Math", "Lecture", 2, 3),
        Course("Drown", "CA1", "Math", "P", 3, 3),
        Course("Jones", "CA2", "Calculus", "Lecture", 2, 3),
        Course("Jones", "CA2", "Calculus", "P", 2, 3),
        Course("Brown", "CA2", "Data Structures", "Lecture", 1, 3),
        Course("Davis", "CA2", "Linear Algebra", "Lecture", 5, 3),
        Course("Davis", "CA2", "Algorithms", "Lecture", 2, 3),
        Course("Johnson", "MATH3", "Math", "Lecture", 3, 2),
        Course("Johnson", "MATH3", "Math", "P", 3, 2),
        Course("Williams", "MATH3", "Statistics", "Lecture", 4, 2),
        Course("Williams", "MATH3", "Statistics", "P", 4, 2),
        Course("Jones", "MATH3", "Algorithms", "Lecture", 1, 3),
        Course("Wilson", "PM1", "English", "Lecture", 2, 2),
        Course("Wilson", "PM1", "English", "P", 2, 2),
        Course("Williams", "PM1", "Statistics", "Lecture", 4, 2),
        Course("Williams", "PM1", "Statistics", "P", 4, 2),
        Course("Smith", "PM1", "History", "P", 1, 3),
        Course("Smith", "PM1", "History", "Lecture", 1, 3),

    ]
    return classes
def load_rooms():
    rooms = [
        Room("RoomA", "Lecture"),
        Room("RoomB", "Lecture"),
        Room("Room9", "Lecture"),
        Room("Room6", "P"),
        Room("Room10", "Lecture"),
        Room("Room11", "P"),
        Room("Room12", "P"),
        Room("Room13", "P"),
        Room("Room14", "Lecture"),
        Room("Room15", "Lecture"),
    ]
    return rooms

rooms = load_rooms()
classes=load_classes()
specializations = group_classes_by_specialization(classes)

def get_num_hours(timetable, subject, day):
    num = 0
    hours = []
    for timeslot, class_info in timetable.final[day].items():
        if class_info and subject.subject == class_info.subject and subject.typeOfClass == class_info.typeOfClass:
            num += 1
            hours.append(timeslot)
    return num, hours

timetable_custom = TimetableCustom(name="My Timetable", num_specializations=len(specializations))

def init_timetable(classes, rooms, timetable_custom):
    individual = []
    max_attempts_per_class = 100

    for specialization, class_objs in specializations.items():
        timetable_custom = TimetableCustom("My Timetable", num_specializations=len(specializations))

        for class_obj in class_objs:
            attempts = 0
            assigned_classes = 0
            total_classes_per_week = class_obj.number

            while attempts < max_attempts_per_class and assigned_classes < total_classes_per_week:
                room = random.choice(rooms)
                day = random.choice([day for day in WeekDay if day != WeekDay.SAT and day != WeekDay.SUN])
                timeslot = random.choice(list(timetable_custom.final[day.name.lower()].keys()))
                if not timetable_custom.final[day.name.lower()][timeslot] and class_obj.typeOfClass == room.type:
                    timetable_custom.final[day.name.lower()][timeslot] = class_obj
                    individual.append((class_obj, room, day, timeslot))
                    assigned_classes += 1

                attempts += 1

            if assigned_classes < total_classes_per_week:
                print("Не вдалося призначити всі заняття для курсу:", class_obj)

                class_obj.number = assigned_classes

    return individual
def fitness(individual, classes, rooms, timetable_custom):
    fitness_score = 0
    penalty_score = 0
    room_occupancy = {room: [] for room in rooms}
    professor_assignments = {professor: {specialization: [] for specialization in set(class_obj.course for class_obj in classes)}
                             for professor in set(class_obj.professor for class_obj in classes if isinstance(class_obj, Course))}

    specializations = group_classes_by_specialization(classes)
    specialization_timetables = {name: TimetableCustom(name, len(specializations)) for name in specializations.keys()}

    for class_obj, room, day, timeslot in individual:
        if timeslot > 1:
            prev_class_obj = timetable_custom.final[day.name.lower()][timeslot - 1]
            if prev_class_obj and prev_class_obj.professor == class_obj.professor and prev_class_obj.subject == class_obj.subject:
                penalty_score += 10

        if (day, timeslot) in room_occupancy[room]:
            penalty_score += 10

        else:
            room_occupancy[room].append((day, timeslot))

        for specialization, assignments in professor_assignments[class_obj.professor].items():
            for assignment_day, assignment_timeslot in assignments:
                if assignment_day == day and assignment_timeslot == timeslot:
                    penalty_score += 30

        professor_assignments[class_obj.professor][class_obj.course].append((day, timeslot))

        timetable_custom.final[day.name.lower()][timeslot] = class_obj

        specialization_timetables[class_obj.course].final[day.name.lower()][timeslot] = class_obj

        if class_obj.typeOfClass == "Lecture" and room.type != "Lecture":
            penalty_score += 20
        elif class_obj.typeOfClass == "P" and room.type != "P":
            penalty_score += 20

    for specialization, timetable in specialization_timetables.items():
        for class_obj in specializations[specialization]:
            for day in WeekDay:
                if day != WeekDay.SAT and day != WeekDay.SUN:
                    num_hours, _ = get_num_hours(timetable, class_obj, day.name.lower())
                    if num_hours < class_obj.number:
                        penalty_score += (class_obj.number - num_hours) * class_obj.duration
                    else:
                        fitness_score += num_hours * class_obj.duration

    return fitness_score, penalty_score





MAX_ATTEMPTS = 10

def mutate_timetable(individual, classes, rooms, timetable_custom):
    for i in range(len(individual)):
        if random.random() < 0.1:
            j = random.randint(0, len(individual) - 1)
            new_room = random.choice(rooms)
            new_day = random.choice([day for day in WeekDay if day!= WeekDay.SAT and day!= WeekDay.SUN])
            attempts = 0
            while attempts < MAX_ATTEMPTS:
                new_timeslot = random.choice(list(timetable_custom.final[new_day.name.lower()].keys()))
                if not timetable_custom.final[new_day.name.lower()][new_timeslot]:
                    individual[i] = (individual[i][0], new_room, new_day, new_timeslot)
                    break
                attempts += 1

    return individual
def crossover(ind1, ind2):
    size = len(ind1)
    crossover_point = random.randint(1, size - 1)
    child1 = ind1[:crossover_point] + ind2[crossover_point:]
    child2 = ind2[:crossover_point] + ind1[crossover_point:]
    return child1, child2
def generate_timetable(classes, rooms, timetable_custom, num_specializations, population_size):
    fitness_scores = []
    penalty_scores = []
    population = []
    for _ in range(population_size):
        individual = init_timetable(classes, rooms, timetable_custom)
        population.append(individual)
    for individual in population:
        fitness_score, penalty_score = fitness(individual, classes, rooms, timetable_custom)
        fitness_scores.append(fitness_score)
        penalty_scores.append(penalty_score)
    for _ in range(1):
        new_population = []
        for _ in range(population_size // 2):
            ind1, ind2 = random.sample(population, 2)
            child1, child2 = crossover(ind1, ind2)
            child1 = mutate_timetable(child1, classes, rooms, timetable_custom)
            child2 = mutate_timetable(child2, classes, rooms, timetable_custom)
            new_population.extend([child1, child2])
        population = new_population
        fitness_scores = []
        penalty_scores = []
        for individual in population:
            fitness_score, penalty_score = fitness(individual, classes, rooms, timetable_custom)
            fitness_scores.append(fitness_score)
            penalty_scores.append(penalty_score)
    best_index = fitness_scores.index(max(fitness_scores))
    best_individual = population[best_index]
    best_fitness_score = fitness_scores[best_index]
    best_penalty_score = penalty_scores[best_index]
    best_individual_dict = individual_to_dict(best_individual, classes, rooms, num_specializations)
    return best_individual_dict, best_fitness_score, best_penalty_score


def individual_to_dict(individual, classes, rooms, num_specializations):
    timetable = TimetableCustom("generated", num_specializations)

    for class_obj, room, day, timeslot in individual:
        timetable.final[day.name.lower()][timeslot] = {
            'class': class_obj,
            'room': room
        }
    return timetable
def timetable_to_dict(timetable):
        timetable_dict = {}
        for day, slots in timetable.final.items():
            timetable_dict[day] = {}
            for timeslot, slot in slots.items():
                if slot:
                    class_obj = slot['class']
                    room = slot['room']
                    timetable_dict[day][timeslot] = {
                        'professor': class_obj.professor,
                        'course': class_obj.course,
                        'subject': class_obj.subject,
                        'typeOfClass': class_obj.typeOfClass,
                        'number': class_obj.number,
                        'duration': class_obj.duration,
                        'room': room.name  # Отримання назви кімнати
                    }
                else:
                    timetable_dict[day][timeslot] = None
        return timetable_dict

def main():
    classes = load_classes()
    rooms = load_rooms()
    population_size=50
    best_individual, best_fitness_score, best_penalty_score = generate_timetable(classes, rooms, timetable_custom,
                                                                                 len(specializations), population_size)

    timetable_dict = timetable_to_dict(best_individual)

    for specialization, classes in group_classes_by_specialization(load_classes()).items():
        filename = f"timetable_{specialization}.txt"
        with open(filename, "w") as file:
            file.write(f"Timetable for Specialization: {specialization}\n\n")
            for day, slots in timetable_dict.items():
                file.write(day.capitalize() + ":\n")
                slot_number = 1
                for timeslot, slot_info in slots.items():
                    if slot_info and slot_info['course'] == specialization:
                        file.write(
                            f"  Time: {slot_number}, Professor: {slot_info['professor']}, Course: {slot_info['course']}, Subject: {slot_info['subject']}, Type of Class: {slot_info['typeOfClass']}, Number: {slot_info['number']}, Duration: {slot_info['duration']}, Room: {slot_info['room']}\n")
                        slot_number += 1
                file.write("\n")
    with open("timetable.txt", "w") as file:
        for day, slots in timetable_dict.items():
            file.write(day.capitalize() + ":\n")
            for timeslot, slot_info in slots.items():
                if slot_info:
                    file.write(
                        f"  Time: {timeslot}, Professor: {slot_info['professor']}, Course: {slot_info['course']}, Subject: {slot_info['subject']}, Type of Class: {slot_info['typeOfClass']}, Number: {slot_info['number']}, Duration: {slot_info['duration']}, Room: {slot_info['room']}\n")
                else:
                    file.write(f"  Time: {timeslot}, No class scheduled\n")
            file.write("\n")

    print("Best fitness score:", best_fitness_score)
    print("Best penalty score:", best_penalty_score)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")