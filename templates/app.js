const API_URL = 'https://jsonplaceholder.typicode.com/todos';






// GET todos
async function getTodos() {
  const res = await fetch(API_URL);
  const data = await res.json();
  console.log(data);
}

// POST new todo
async function addTodo(title) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, completed: false })
  });
  const data = await res.json();
  console.log('Added:', data);
}

// PUT update todo
async function updateTodo(id, completed) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed })
  });
  const data = await res.json();
  console.log('Updated:', data);
}

// DELETE todo
async function deleteTodo(id) {
  await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  console.log(`Deleted todo ${id}`);
}

getTodos(); // Example call
