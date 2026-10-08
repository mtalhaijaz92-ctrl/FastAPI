from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Student Management API",
    description="A beginner-friendly REST API built with FastAPI",
    version="1.0.0"
)


# -----------------------------
# Pydantic Model
# -----------------------------

class Student(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(gt=0, lt=100)
    city: str


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    age: Optional[int] = Field(default=None, gt=0, lt=100)
    city: Optional[str] = None


# -----------------------------
# Temporary Data
# -----------------------------

students = {
    1: {
        "id": 1,
        "name": "Talha",
        "age": 20,
        "city": "Gujranwala"
    },
    2: {
        "id": 2,
        "name": "Ali",
        "age": 21,
        "city": "Lahore"
    }
}


# -----------------------------
# GET - All Students
# -----------------------------

@app.get("/students")
def get_students(city: Optional[str] = None):

    if city:
        result = []

        for student in students.values():
            if student["city"].lower() == city.lower():
                result.append(student)

        return result

    return list(students.values())


# -----------------------------
# GET - Single Student
# -----------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]


# -----------------------------
# POST - Create Student
# -----------------------------

@app.post("/students", status_code=201)
def create_student(student: Student):

    new_id = max(students.keys(), default=0) + 1

    students[new_id] = {
        "id": new_id,
        "name": student.name,
        "age": student.age,
        "city": student.city
    }

    return {
        "message": "Student created successfully",
        "student": students[new_id]
    }


# -----------------------------
# PUT - Update Complete Student
# -----------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student
):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = {
        "id": student_id,
        "name": student.name,
        "age": student.age,
        "city": student.city
    }

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


# -----------------------------
# PATCH - Partial Update
# -----------------------------

@app.patch("/students/{student_id}")
def partial_update(
    student_id: int,
    student: StudentUpdate
):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if student.name is not None:
        students[student_id]["name"] = student.name

    if student.age is not None:
        students[student_id]["age"] = student.age

    if student.city is not None:
        students[student_id]["city"] = student.city

    return {
        "message": "Student partially updated",
        "student": students[student_id]
    }


# -----------------------------
# DELETE - Student
# -----------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "student": deleted_student
    }

