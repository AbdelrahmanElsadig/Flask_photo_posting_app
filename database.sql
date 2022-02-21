CREATE TABLE users (
    user_id BIGSERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    user_password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    pfp VARCHAR (255) DEFAULT ''
);

CREATE TABLE posts (
    post_id BIGSERIAL NOT NULL PRIMARY KEY,
    caption TEXT NOT NULL,
    post_img VARCHAR(255) NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes BIGINT DEFAULT 0,
    user_id BIGINT NOT NULL REFERENCES users(user_id)
);

CREATE TABLE likes (
    user_id BIGINT REFERENCES users(user_id),
    post_id BIGINT REFERENCES posts(post_id),
    is_like NUMERIC DEFAULT 0
)