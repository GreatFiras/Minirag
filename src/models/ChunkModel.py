from .BaseDataModel import BaseDataModel 
from .db_schemes import DataChunk
from .enums.DataBaseEnums import DataBaseEnum
from pymongo import InsertOne
#cuz we will get a chunk from the monogo-db ; when we get from mongo we use ObjectId cuz we are inside the mongo , 
# when we are outside the mongo , convert it to string ; 

from bson.objectid import ObjectId 

class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    
    #creating chunks 

    async def create_chunk( self , chunk : DataChunk ): 

        result = await self.collection.insert_one(chunk.dict(by_alias=True , exclude_unset=True))
        chunk._id = result.inserted_id 

        return chunk
    
    async def get_chunk (self , chunk_id: str ): 
        result = await self.collection.find_one({
            "_id" : ObjectId(chunk_id) , 
        })

        if result is None: 
            return None
        
        return DataChunk(** result)
    
    
    async def insert_many_chunk(self , chunks: list , batch_size : int = 100 ): 

        for i in range(0 , len(chunks) , batch_size): 
            batch = chunks[i:i+batch_size]

            operations = [

                InsertOne(chunks.dict(by_alias=True , exclude_unset=True))
                for chunks in batch
            ]

            await self.collection.insert_many(operations)
        return len(chunks)
    
    async def delete_chunk_by_project_id (self , project_id : ObjectId): 

        result = await self.collection.delete_many({
            "chunk_project_id" : project_id})
        
        return result.deleted_count


