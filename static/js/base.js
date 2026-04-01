$(document).ready(function() {
    // CSRF setup for AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Like button handler
    $('.like-btn').click(function(e) {
        e.preventDefault();
        const postId = $(this).data('post-id');
        const icon = $(`#like-icon-${postId}`);
        const count = $(`#like-count-${postId}`);

        $.ajax({
            url: `/like/${postId}/`,
            method: 'GET',
            success: function(data) {
                if (data.liked) {
                    icon.removeClass('fa-regular').addClass('fa-solid');
                    icon.css('color', '#e74c3c');
                } else {
                    icon.removeClass('fa-solid').addClass('fa-regular');
                    icon.css('color', 'inherit');
                }
                count.text(data.total_likes);
            }
        });
    });

    // Comment form handler
    $('.comment-form').submit(function(e) {
        e.preventDefault();
        const form = $(this);
        const postId = form.data('post-id');
        const list = $(`#comments-list-${postId}`);
        const input = form.find('input[name="text"]');

        $.ajax({
            url: `/comment/${postId}/`,
            method: 'POST',
            data: form.serialize(),
            headers: { 'X-CSRFToken': csrftoken },
            success: function(data) {
                list.append(`
                    <div class="comment">
                        <strong>${data.username}</strong> ${data.text}
                    </div>
                `);
                input.val('');
            }
        });
    });

    // Follow button handler
    $(document).on('click', '.follow-btn', function(e) {
        e.preventDefault();
        const username = $(this).data('username');
        const btn = $(this);

        $.ajax({
            url: `/follow/${username}/`,
            method: 'GET',
            success: function(data) {
                if (data.followed) {
                    btn.text('Unfollow');
                    btn.css({'background': 'transparent', 'border': '1px solid #ddd', 'color': 'var(--primary-color)'});
                } else {
                    btn.text('Follow');
                    btn.css({'background': 'var(--primary-color)', 'border': 'none', 'color': 'white'});
                }
            }
        });
    });
});

function togglePostMenu(postId) {
    const menu = document.getElementById(`post-menu-${postId}`);
    if (menu.style.display === 'none' || menu.style.display === '') {
        // Close other menus first
        document.querySelectorAll('[id^="post-menu-"]').forEach(m => m.style.display = 'none');
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

// Close menus on outside click
window.addEventListener('click', function(event) {
    if (!event.target.matches('.fa-ellipsis') && !event.target.matches('.fa-ellipsis-h') && !event.target.closest('.custom-dropdown')) {
        document.querySelectorAll('[id^="post-menu-"]').forEach(m => {
            m.style.display = 'none';
        });
    }
});
