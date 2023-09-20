from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# we extend BaseModel class and define variables, pydantic will check incoming payload for listed fields in body.
# if field is not available or it's not a string, it will throw a validation error
class Post(BaseModel):
    title:  str
    content: str
    # default set to true
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content" : "content of post 1", "id": 1}, {"title":  "title of post 2", "content": "content of post 2", "id": 2 }]


def find_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return post, index
    return None, -1 # return None and -1 if the post is not found

def del_post(id):
    #enumerate returns pairs of '(index, p)'
    post, index = find_post(id)
    if index is not None:
        del my_posts[index]
        return True
    else:
        return False

def upd_post(id, post_to_dict):
    post, index = find_post(id)
    if index is not None:
        my_posts[index] = post_to_dict
        return True
    else:
        return False

# decorator on line 6 turns a simple function to a api path
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #converts pydantic model to a dictionary
    post_to_dict = post.model_dump()
    post_to_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_to_dict)
    return {"data": post_to_dict}

@app.get("/posts/{id}")
#strong type parameter, so api returns a validation error if non int
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} was not found")
    else:
        return {"message": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = del_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} was not found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    post_to_dict = post.model_dump()
    post_to_dict['id'] = id
    post = upd_post(int(id), post_to_dict)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} was not found")
    else:
        return {"message": post_to_dict}






 
 