// ============================================================
// script.js  –  Student Tech Hub Frontend Logic
// Plain JavaScript – no libraries or frameworks needed!
// ============================================================

// The URL of our FastAPI backend server.
// Change this if your backend runs on a different port.
const API_BASE_URL = "http://127.0.0.1:8000";

// ---------------------------------------------------------------
// FUNCTION: loadEvents()
// Called when the user clicks the "Load Events from Server" button.
// It fetches events from GET /api/events and displays them.
// ---------------------------------------------------------------
async function loadEvents() {
  const btn         = document.getElementById("load-events-btn");
  const statusMsg   = document.getElementById("events-status");
  const eventsList  = document.getElementById("events-list");

  // --- Show a loading state ---
  btn.disabled = true;
  btn.textContent = "⏳ Loading…";
  setStatus(statusMsg, "loading", "Fetching events from the server…");
  eventsList.innerHTML = ""; // Clear any previously loaded events

  try {
    // Make a GET request to the backend
    const response = await fetch(`${API_BASE_URL}/api/events`);

    // If the response isn't OK (e.g. 500 error), throw an error
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    // Parse the JSON data returned by the backend
    const data = await response.json();

    // Check if the backend reported success
    if (data.success && data.events.length > 0) {
      setStatus(statusMsg, "success", `✅ ${data.count} events loaded successfully!`);
      renderEvents(data.events); // Build and show event cards
    } else {
      setStatus(statusMsg, "error", "No events found.");
    }

  } catch (error) {
    // This runs if the network is down or the backend isn't running
    setStatus(
      statusMsg,
      "error",
      "❌ Could not connect to the server. Make sure the backend is running on port 8000."
    );
    console.error("loadEvents error:", error);
  } finally {
    // Re-enable the button regardless of success or failure
    btn.disabled = false;
    btn.textContent = "🔄 Load Events from Server";
  }
}

// ---------------------------------------------------------------
// FUNCTION: renderEvents(events)
// Takes an array of event objects and builds HTML cards for each.
// ---------------------------------------------------------------
function renderEvents(events) {
  const eventsList = document.getElementById("events-list");
  eventsList.innerHTML = ""; // Clear previous content

  events.forEach(function(event) {
    // Build one card per event using a template literal
    const card = document.createElement("div");
    card.className = "event-card";
    card.innerHTML = `
      <h3>${event.title}</h3>
      <div class="event-meta">
        <span>📅 ${formatDate(event.date)} &nbsp;·&nbsp; ⏰ ${event.time}</span>
        <span>📍 ${event.location}</span>
      </div>
      <p style="font-size:0.875rem; color:#475569; margin-bottom:12px;">${event.description}</p>
      <span class="event-badge">${event.category}</span>
    `;
    eventsList.appendChild(card);
  });
}

// ---------------------------------------------------------------
// FUNCTION: registerStudent(event)
// Called when the registration form is submitted.
// It sends the student's name and email to POST /api/register.
// ---------------------------------------------------------------
async function registerStudent(formEvent) {
  // Prevent the browser from refreshing the page on form submit
  formEvent.preventDefault();

  const nameInput   = document.getElementById("student-name");
  const emailInput  = document.getElementById("student-email");
  const statusMsg   = document.getElementById("register-status");
  const btn         = document.getElementById("register-btn");

  const name  = nameInput.value.trim();
  const email = emailInput.value.trim();

  // Basic client-side validation
  if (!name || !email) {
    setStatus(statusMsg, "error", "Please fill in both your name and email.");
    return;
  }

  // --- Show a loading state ---
  btn.disabled = true;
  btn.textContent = "⏳ Registering…";
  setStatus(statusMsg, "loading", "Sending your details to the server…");

  try {
    // Make a POST request with JSON body
    const response = await fetch(`${API_BASE_URL}/api/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",  // Tell the server we're sending JSON
      },
      body: JSON.stringify({ name: name, email: email }),  // Convert JS object → JSON string
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      setStatus(statusMsg, "success", data.message);
      // Clear the form inputs on success
      nameInput.value  = "";
      emailInput.value = "";
    } else {
      setStatus(statusMsg, "error", `⚠️ ${data.message}`);
    }

  } catch (error) {
    setStatus(
      statusMsg,
      "error",
      "❌ Could not connect to the server. Make sure the backend is running on port 8000."
    );
    console.error("registerStudent error:", error);
  } finally {
    btn.disabled = false;
    btn.textContent = "✅ Register Now";
  }
}

// ---------------------------------------------------------------
// HELPER: setStatus(element, type, message)
// Updates a status message element with a styled message.
// type can be: "loading" | "success" | "error"
// ---------------------------------------------------------------
function setStatus(element, type, message) {
  element.textContent  = message;
  element.className    = `status-msg ${type}`; // CSS class controls the colour
}

// ---------------------------------------------------------------
// HELPER: formatDate(dateStr)
// Converts "2026-10-10" → "October 10, 2026" for display.
// ---------------------------------------------------------------
function formatDate(dateStr) {
  const options = { year: "numeric", month: "long", day: "numeric" };
  // We append T00:00:00 to avoid timezone shifting the date by one day
  const date = new Date(dateStr + "T00:00:00");
  return date.toLocaleDateString("en-IN", options);
}
