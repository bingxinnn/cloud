(function($) {

	"use strict";

	$('[data-toggle="tooltip"]').tooltip()

})(jQuery);


/*===== LOGIN SHOW and HIDDEN =====*/
// Get a reference to the button element
const button = document.getElementById('returnComp-id');

// Add a click event listener to the button
button.addEventListener('click', function() {
    // Redirect to another HTML page
        window.location.href = 'home.html';
    });