import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../api/auth';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      try {
        const data = await getCurrentUser(token);
        setUser(data.user);
      } catch (err) {
        // Token likely invalid or expired
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      }
    };

    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Welcome, {user.username}!</h2>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>

      <div className="user-card">
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Account created:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
      </div>

      {user.role === 'admin' && (
        <div className="admin-badge">
          🔒 You have admin privileges
        </div>
      )}
    </div>
  );
}

export default Dashboard;