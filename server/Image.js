import React from 'react';
import './App.css';
const response = [{"image_id": "1", "street": "1317 Van Buren Avenue" , "citi" : "Salton City, CA", "bed" : "3", "bath" : "2", "sqft" : "1560", "price": "$201900"}, {"image_id": "1", "street": "1317 Van Buren Avenue" , "citi" : "Salton City, CA", "bed" : "3", "bath" : "2", "sqft" : "1560", "price": "$201900"}];
function ImageList({ imageIds }) {
    return (
      <div style={{display: 'flex', justifyContent: 'left'}}>
        <table class="rwd-table">
        <tr>
        <th></th>
        <th>Listing Details</th>
        </tr>
        {response.map((id) => (
            <tr>
                <td data-th="Property Title"><img
               src={require(`./archive/socal2/socal_pics/${id.image_id}.jpg`)} // Replace with the actual path to your images
               alt={`Image ${id}`}
               style={{ maxWidth: '100%', height: 'auto', display: 'flex', justifyContent: 'left', marginRight: '20px', margin: '10%'}}
             /> </td>
                <td data-th="Genre">
                        <div style={{margin:'10%'}}>

                        <p>Address: {id.street}, {id.citi}</p>
                         <p>Bedrooms: {id.bed}</p>
                         <p>Bathrooms: {id.bath}</p>
                         <p>Square-feet: {id.sqft}</p>
                         <p>Price:{id.price}</p>
                         </div></td>
            </tr>
        //   <div key={id} style={{ marginBottom: '16px', marginRight: '20px', display: 'flex', flexDirection: 'row'}}>
        //     <img
        //       src={require(`./archive/socal2/socal_pics/${id}.jpg`)} // Replace with the actual path to your images
        //       alt={`Image ${id}`}
        //       style={{ maxWidth: '100%', height: 'auto', display: 'flex', justifyContent: 'left', marginRight: '20px'}}
        //     /> 
        //         <div style={{display: 'flex', flexDirection: 'column'}}> 
        //         <p>Address:</p>
        //         <p>Bedrooms:</p>
        //         <p>Bathrooms:</p>
        //         </div>
        //   </div>
        // <tr>
        
        ))}
        </table>
      </div>
    );
  }
  
  export default ImageList;