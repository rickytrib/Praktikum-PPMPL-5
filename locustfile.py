from locust import HttpUser, TaskSet, task, between
import random
import json

# Data contoh untuk pengujian
sample_data = {
    "name": "Item Test",
    "description": "This is a test item"
}

class APITestUser(HttpUser):
    wait_time = between(1, 5)  # waktu tunggu antara setiap tugas

    @task(1)
    def create_item(self):
        # POST request untuk membuat item baru
        response = self.client.post("/items", json=sample_data)
        if response.status_code == 201:
            # Simpan ID item yang baru dibuat untuk pengujian lainnya
            item_id = response.json().get("id")
            if item_id:
                self.item_id = item_id

    @task(2)
    def get_items(self):
        # GET request untuk mendapatkan semua item
        self.client.get("/items")

    @task(3)
    def get_single_item(self):
        # GET request untuk mendapatkan satu item berdasarkan ID
        if hasattr(self, 'item_id'):
            self.client.get(f"/items/{self.item_id}")

    @task(4)
    def update_item(self):
        # PUT request untuk memperbarui item
        if hasattr(self, 'item_id'):
            updated_data = {
                "name": "Updated Item Test",
                "description": "This is an updated test item"
            }
            self.client.put(f"/items/{self.item_id}", json=updated_data)

    @task(5)
    def delete_item(self):
        # DELETE request untuk menghapus item
        if hasattr(self, 'item_id'):
            self.client.delete(f"/items/{self.item_id}")
            del self.item_id  # hapus ID untuk mencegah penghapusan berulang

# User class yang akan melakukan pengujian
class APIUser(HttpUser):
    tasks = [APITestUser]
    wait_time = between(1, 3)
