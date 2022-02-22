if (document.URL.includes("/posts")) {
    get_posts();
    setTimeout(like_color(),5000)
}
if (document.URL.includes("/posts/my_posts")) {
    let drop = document.querySelector('.dropdown');
    drop.remove()
}

function like_color(){
    fetch('/likes')
    .then(res => {return res.json()})
    .then(data => {
        for (let i=0; i < data.length;i++){
            let id = data[i]['post_id'];
            let post = document.getElementById('' + id);
            let heart = post.querySelector('.bi-heart-fill');
            heart.classList.add('red');
        }
    })
}
function add_likes(icon,likes,id){
    icon.addEventListener('click',() =>{
        if (!icon.classList.contains('red')){
            icon.classList.add('red');
            likes.textContent = (1 + parseInt(likes.textContent)).toString()
            let info = {post_id: id}
            fetch('/likes',{
                method: 'post',
                headers: {
                    'Accept': 'application/json'
                  },
                body: JSON.stringify(info)
            })
            .then(res => {return res.json()})
            .then(data => console.log(data))
        }
    })
    
}


function Signup(){
    let data = document.querySelector('.register-form');
    let form = new FormData(data)
    fetch('/signup',{
        method: 'post',
        body: form
    })
    .then(res => {return res.json()})
    .then(info => {
        if ('msg' in info){
            let h3 = document.createElement('h3');
            h3.classList.add('lead');
            h3.textContent = info['msg']
            let error = document.querySelector('.lead');
            if (error !== null){
                error.remove()
            };
            data.appendChild(h3)
        }
        else {
            window.location.href = '/posts'
        }

    })
    return false
};

function logging(){
    let info = document.querySelector('.login-form');
    let form = new FormData(info);
    fetch('/log',{
        method: 'post',
        body: form
    })
    .then(res => {return res.json()})
    .then(data => {
        if ('msg' in data){
            let h3 = document.createElement('h3');
            h3.classList.add('lead');
            h3.textContent = data['msg']
            let error = document.querySelector('.lead');
            if (error !== null){
                error.remove()
            };
            info.appendChild(h3)
        }
        else {
            window.location.href = '/posts'
        }
    })
    return false
}

function make_post(){
    let form_location = document.querySelector('.create');
    let form = new FormData(form_location);
    fetch('/post_creation',{
        method: 'post',
        body: form
    })
    .then(res => {
        if (res.status == '500'){
            return {'msg':'Internal server error'}
        }
        else {
            return res.json()
        }
    })
    .then(data => {
            if ('msg' in data){
                let h3 = document.createElement('h3');
                h3.classList.add('lead');
                h3.textContent = data['msg']
                let error = document.querySelector('.lead');
                if (error !== null){
                    error.remove()
                };
                form_location.appendChild(h3)
            }
            else {
                window.location.href = '/posts'
            }
    })
    return false
}

function get_posts(){
    let request_link = '/post_creation'
    if (document.URL.includes("/posts/likes")){
        request_link = '/likes_sort'
    }
    else if (document.URL.includes("/posts/my_posts")){
        request_link = '/my_posts'
    }
    fetch(request_link)
    .then(res => {return res.json()})
    .then(data => {
        for (let i = 0; i < data.length; i++){
            let username = data[i]['username'];
            let pfp_path = data[i]['pfp'];
            let timestamp = data[i]['post_date'];
            let caption = data[i]['caption'];
            let post_image_path = data[i]['post_img'];
            let likes_sum = data[i]['likes'];
            let id = data[i]['post_id'];
            send_post(username,pfp_path,timestamp,caption,post_image_path,likes_sum,id)
        }
    })
}

function send_post(username,pfp_path,timestamp,caption,post_image_path,likes_sum,id){
    let all_posts = document.querySelector('.posts')
    let post = document.createElement('div');
    post.classList.add('post');
    post.id = id;
    all_posts.appendChild(post);

    let info = document.createElement('div');
    info.classList.add('info')
    post.appendChild(info);

    let pfp = document.createElement('img');
    if (pfp_path === ''){
        pfp.setAttribute('src','../static/images/user-circle.svg');
    }
    else{pfp.setAttribute('src',pfp_path);}
    info.appendChild(pfp);

    let name = document.createElement('h1');
    info.appendChild(name);
    name.textContent = username;

    let date = document.createElement('p');
    date.textContent = timestamp;
    info.appendChild(date);

    let text = document.createElement('p')
    text.classList.add('text');
    text.textContent = caption
    post.appendChild(text);

    let image = document.createElement('img');
    image.classList.add('post-image');
    image.setAttribute('src',post_image_path);
    post.appendChild(image);
    
    let feedback = document.createElement('div');
    feedback.classList.add('feedback');
    post.appendChild(feedback);

    let icon = document.createElement('i');
    icon.classList.add('bi');
    icon.classList.add('bi-heart-fill');
    feedback.append(icon);
    

    let likes = document.createElement('p');
    likes.classList.add('likes');
    likes.textContent = likes_sum;
    add_likes(icon,likes,id)
    feedback.appendChild(likes);
    feedback.append('Likes')
}

function edit(){
    let data = document.querySelector('.edit-form');
    let form = new FormData(data);
    fetch('/edit',{
        method: 'post',
        body: form
    })
    .then(res => {return res.json()})
    .then(info => {
        if ('msg' in info){
            let h3 = document.createElement('h3');
            h3.classList.add('lead');
            h3.textContent = info['msg']
            let error = document.querySelector('.lead');
            if (error !== null){
                error.remove()
            };
            data.appendChild(h3)
        }
        else {
            window.location.href = '/posts'
            console.log(info)
        }
    })
    return false
}