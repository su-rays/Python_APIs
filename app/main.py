from fastapi import FastAPI, HTTPException, status, Response

from .schemas import Post

from .database import conn, cursor

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    my_post = cursor.fetchall()
    print(my_post)
    return {"data": my_post}

@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id),))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=404, detail="post not found")
    return {"post_detail": test_post}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")
    return {"data": updated_post}

@app.options("/posts")
def options_post():
    return Response(headers={"Allow": "GET, POST, PATCH, HEAD, OPTIONS"}, status_code=204)