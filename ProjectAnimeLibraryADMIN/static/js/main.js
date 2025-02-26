document.addEventListener('DOMContentLoaded', function() {
    // Logout functionality
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();

            if (confirm('Are you sure you want to log out?')) {
                window.location.href = "/logout";
            }
        });
    }

    // Bookmark functionality
    const favoriteButtons = document.querySelectorAll('.favorite');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.card');
            const bookmarkData = {
                name: card.getAttribute('data-name'),
                site: card.querySelector('p:nth-child(2)').innerText,
                video: card.querySelector('p:nth-child(3)').innerText,
                link: card.querySelector('a').getAttribute('href')
            };

            fetch('/add_bookmark', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bookmarkData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Bookmark added successfully!');
                } else {
                    alert('Error adding bookmark: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Sorting functionality
    document.getElementById('asc').addEventListener('click', function() {
        sortCards('asc');
    });

    document.getElementById('desc').addEventListener('click', function() {
        sortCards('desc');
    });

    // Search functionality
    document.getElementById('search-input').addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const cards = document.querySelectorAll('.card');

        cards.forEach(card => {
            const name = card.querySelector('h2').innerText.toLowerCase();
            if (name.includes(query)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Delete functionality with confirmation prompt
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const card = event.target.closest('.card');
            const bookmarkName = card.querySelector('h2').innerText;
            const confirmed = confirm(`Are you sure you want to delete the bookmark "${bookmarkName}"?`);

            if (confirmed) {
                const bookmarkId = card.getAttribute('data-id');

                fetch(`/delete_bookmark/${bookmarkId}`, {
                    method: 'DELETE'
                })
                .then(response => {
                    if (response.ok) {
                        card.remove();
                    } else {
                        console.error('Failed to delete bookmark');
                    }
                })
                .catch(error => console.error('Error deleting bookmark:', error));
            } else {
                event.preventDefault();
            }
        });
    });

    function sortCards(order) {
        const cardsContainer = document.querySelector('.bookmarks-list');
        const cards = Array.from(cardsContainer.children);

        cards.sort((a, b) => {
            const nameA = a.querySelector('h2').innerText.toLowerCase();
            const nameB = b.querySelector('h2').innerText.toLowerCase();

            if (order === 'asc') {
                return nameA.localeCompare(nameB);
            } else {
                return nameB.localeCompare(nameA);
            }
        });

        cards.forEach(card => cardsContainer.appendChild(card));
    }
});
