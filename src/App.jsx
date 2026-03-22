import { useState } from 'react'
import './App.css'

function App() {
  // date and all
  const [formData, setFormData] = useState({
    name: '',
    cron: '',
    nextRun: '',
    startDate: '',
    endDate: ''
  })

  // put changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  }

  // form submit 
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // going to fast api
    console.log("Data ready to send to FastAPI:", formData);

    try {
      const response = await fetch('http://localhost:8000/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      alert("Task submitted successfully! Check console for payload.");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  return (
    <div className="form-container">
      <h2>Create Periodic Task</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '400px', margin: '0 auto' }}>
        
        <div>
          <label>Task Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>

        <div>
          <label>Cron Expression:</label>
          <input type="text" name="cron" value={formData.cron} onChange={handleChange} required />
        </div>

        <div>
          <label>Next Run:</label>
          <input type="datetime-local" name="nextRun" value={formData.nextRun} onChange={handleChange} required />
        </div>

        <div>
          <label>Start Date:</label>
          <input type="datetime-local" name="startDate" value={formData.startDate} onChange={handleChange} required />
        </div>

        <div>
          <label>End Date:</label>
          <input type="datetime-local" name="endDate" value={formData.endDate} onChange={handleChange} required />
        </div>

        <button type="submit" style={{ padding: '10px', marginTop: '10px', cursor: 'pointer' }}>
          Save Task
        </button>
      </form>
    </div>
  )
}

export default App