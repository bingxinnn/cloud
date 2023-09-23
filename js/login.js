document.getElementById('loginButton').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default form submission behavior

  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  // Extract the role from the email
  let role;
  if (email.endsWith('@student.com')) {
    role = 'student';
    window.location.href = 'user_page.html';
  } else if (email.endsWith('@admin.com')) {
    role = 'admin';
    window.location.href = 'admin.html';
    
  } else if (email.endsWith('@lecturer.com')) {
    role = 'lecturer';
    window.location.href = 'lecture.html';

  } else if (email.endsWith('@company.com')) {
    role = 'company';
    window.location.href = 'index.html';
  } else {
    // Handle unrecognized email pattern or role
    console.error('Unrecognized email pattern or role');
    return;
  }

  // Display a success message with the identified role
  const successMessage = document.createElement('div');
  successMessage.classList.add('alert', 'alert-success');
  successMessage.textContent = `Successfully logged in as ${role}.`;

  // Append the success message to the message container
  const messageContainer = document.getElementById('messageContainer');
  messageContainer.innerHTML = ''; // Clear any previous messages
  messageContainer.appendChild(successMessage);
});
