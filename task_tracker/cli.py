import sys
import json
import os
from datetime import datetime

# definir la ruta del archivo Json
# donde se guardarán las tareas
TASKS_FILE = 'tasks.json'

#funcion para cargar tareas desde el archivo Json
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
    
#funcion para guardar tareas en el archivo Json
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

#estructura base del script
def main():
    args = sys.argv[1:] 

    if not args:
        print("Usage: task_cli.py [add|list|remove] [task details]")
        return
    command = args[0]
    tasks = load_tasks()

    if command == "list":
        if len(args) == 1:
            if not tasks:
                print("No hay tareas registradas.")
            else:
                for task in tasks:
                    print(f"{task['id']}: {task['description']} [{task['status']}]")
        
        elif len(args) == 2 and args[1] == "--verbose":
            if not tasks:
                print("no hay tareas registradas.")
            else:
                for task in tasks:
                    print(f"[{task['id']}] ({task['status']}) {task['description']}")
                    print(f"   ↳ Creado:     {task['created_at']}")
                    print(f"   ↳ Actualizado: {task['updated_at']}")


        else:
            status_filter = args[1]
            valid_statuses = ["todo", "in-progress", "done"]
            if status_filter not in valid_statuses:
                print(f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}")
                return
            filtered_tasks = [t for t in tasks if t["status"] == status_filter]

            if not filtered_tasks:
                print(f"no hay tareas con el estado '{status_filter}'.")
            else:
                for task in filtered_tasks:
                    print(f"{task['id']}: {task['description']} [{task['status']}]")

    elif command == "add":
        if len(args) < 2:
            print("Usage: task_cli.py add [task description]")
            return
        description = args[1]
        now = datetime.now().isoformat()


        # Obtener el próximo ID
        next_id = 1
        if tasks:
            next_id = max(task["id"]for task in tasks)+1

        new_task ={
            "id": next_id,
            "description": description,
            "status": "todo",
            "created_at": now,
            "updated_at": now
        }

        
        tasks.append(new_task)
        save_tasks(tasks)

        print(f"Tarea añadida: {new_task['id']}: {new_task['description']} [{new_task['status']}]")
    
    elif command == "update":
        if len(args) < 3:
            print("Usage: task_cli.py update [task id] [new status]")
            return
        
        try:
            task_id = int(args[1])
        except ValueError:
            print("El ID de la tarea debe ser un número.")
            return
        new_description = args[2]
        task_found = False

        for task in tasks:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updatedAt"] = datetime.now().isoformat()
                task_found = True
                break
        if not task_found:
            print(f"No se encontró la tarea con ID {task_id}.")
        else:
            save_tasks(tasks)
            print(f"Tarea con ID {task_id} actualizada exitosamente.")

    elif command == "delete":
        if len(args) <2:
            print("usage: task_cli.py delete [task id]")
            return
        try:
            task_id = int(args[1])
        except ValueError:
            print("El ID de la tarea debe ser un número.")
            return
        
        original_length = len(tasks)
        tasks = [task for task in tasks if task["id"] != task_id]

        if len(tasks) < original_length:
            save_tasks(tasks)
            print(f"Tarea con ID {task_id} eliminada exitosamente.")
        else:
            print(f"No se encontró la tarea con ID {task_id}.")
    
    elif command == "mark-in-progress":
        if len(args) < 2:
            print("Usage: task_cli.py mark-in-progress [task id]")
            return
        try: 
            task_id = int(args[1])
        except ValueError:
            print("El ID de la tarea debe ser un número.")
            return
        
        task_found = False
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "in-progress"
                task["updated_at"] = datetime.now().isoformat()
                task_found = True
                break
        
        if task_found:
            save_tasks(tasks)
            print(f"Tarea con ID {task_id} marcada como 'in-progress'.")
        else:
            print(f"No se encontró la tarea con ID {task_id}.")


    elif command == "mark-done":
        if len(args) < 2:
            print("Usage: task_cli.py mark-done [task id]")
            return
        try:
            task_id = int(args[1])
        except ValueError:
            print("El ID de la tarea debe ser un número.")
            return
        
        task_found = False
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "done"
                task["updated_at"] = datetime.now().isoformat()
                task_found = True
                break
        if task_found:
            save_tasks(tasks)
            print(f"Tarea con ID {task_id} marcada como 'done'.")
        else:
            print(f"No se encontró la tarea con ID {task_id}.")
    elif command == "help":
        print("Comandos disponibles:")
        print("  add [task description] - Añade una nueva tarea.")
        print("  list [status] - Lista las tareas. Usa 'todo', 'in-progress' o 'done' para filtrar.")
        print("  update [task id] [new description] - Actualiza la descripción de una tarea.")
        print("  delete [task id] - Elimina una tarea por su ID.")
        print("  mark-in-progress [task id] - Marca una tarea como 'in-progress'.")
        print("  mark-done [task id] - Marca una tarea como 'done'.")
        print("  help - Muestra este mensaje de ayuda.")

def run():
    main()
