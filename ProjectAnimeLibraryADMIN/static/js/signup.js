document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    togglePassword?.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });

    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const confirmPassword = document.getElementById('confirm_password');

    toggleConfirmPassword?.addEventListener('click', function () {
        const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPassword.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    const cards = document.querySelectorAll('.card');

    searchInput.addEventListener('input', function() {
        const searchValue = this.value.toLowerCase();
        cards.forEach(card => {
            const cardName = card.getAttribute('data-name').toLowerCase();
            if (cardName.includes(searchValue)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // ascending 
    function sortByNameAsc() {
        const library = document.querySelector('.library');
        const cards = Array.from(library.querySelectorAll('.card'));

        cards.sort((a, b) => {
            const nameA = a.getAttribute('data-name').toUpperCase();
            const nameB = b.getAttribute('data-name').toUpperCase();
            if (nameA < nameB) {
                return -1;
            }
            if (nameA > nameB) {
                return 1;
            }
            return 0;
        });

        library.innerHTML = '';
        cards.forEach(card => library.appendChild(card));
    }

    //  descending 
    function sortByNameDesc() {
        const library = document.querySelector('.library');
        const cards = Array.from(library.querySelectorAll('.card'));

        cards.sort((a, b) => {
            const nameA = a.getAttribute('data-name').toUpperCase();
            const nameB = b.getAttribute('data-name').toUpperCase();
            if (nameA > nameB) {
                return -1;
            }
            if (nameA < nameB) {
                return 1;
            }
            return 0;
        });

        library.innerHTML = '';
        cards.forEach(card => library.appendChild(card));
    }

    document.getElementById('asc').addEventListener('click', sortByNameAsc);
    document.getElementById('desc').addEventListener('click', sortByNameDesc);
});



// Delete Bookmark
$(document).ready(function() {
    $('.delete-button').click(function() {
        var bookmarkId = $(this).closest('.card').data('id');
        $.ajax({
            url: '/delete_bookmark/' + bookmarkId,
            type: 'DELETE',
            success: function(result) {
                // Remove the card from the DOM on success
                $('div[data-id="' + bookmarkId + '"]').remove();
                alert(result.message);
            },
            error: function(xhr, status, error) {
                alert('Error deleting bookmark: ' + error);
            }
        });
    });
});