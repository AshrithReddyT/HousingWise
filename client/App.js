
import './App.css';

import React from 'react';
import ImageList from './Image.js';




function App() {
  const imageIds = [1, 2, 3, 4, 5, 6];
  
  return (
    <div className="App">
      <header className="App-header">

        
        <h1>Property Suggestions</h1>
        
      <div>
      <ImageList imageIds={imageIds} />
      </div>
      </header>
    </div>
  );
}

export default App;
