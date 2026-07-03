# Tianshu Fu - Personal Portfolio Website

Personal portfolio website: https://tianshufu.com/

## Recent Optimizations (2025)

This website has been recently optimized for better performance and maintainability:

### What Was Improved:

1. **Removed Unused JavaScript**
   - Removed jQuery MixItUp plugin (portfolio section removed)
   - Reduced JavaScript bundle size by ~30KB

2. **Upgraded Dependencies**
   - jQuery upgraded from 3.2.1 to 3.7.1 (latest stable)
   - Improved security and performance

3. **Image Optimization**
   - Added lazy loading to images
   - Faster initial page load

4. **Code Modernization**
   - Modernized JavaScript with ES6+ features (const, let, arrow functions)
   - Replaced jQuery-dependent code with vanilla JavaScript where possible
   - Better code organization and readability

5. **CSS Variables**
   - Centralized color scheme with CSS custom properties
   - Easy theme customization
   - Consistent styling across pages

6. **Consolidated Templates**
   - Fixed duplicate HTML in video pages
   - Consistent navigation and footer across all pages
   - Updated copyright to 2025

7. **Build Process**
   - Added npm scripts for development and production builds
   - CSS and JS minification support
   - Image optimization tooling

## Development

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Setup
```bash
# Install dependencies (optional, only needed for build tools)
npm install

# Start local development server
npm start
```

### Available Scripts

- `npm start` - Start local development server on port 8080
- `npm run build` - Build production-ready assets (minify CSS & JS)
- `npm run minify:css` - Minify CSS files
- `npm run minify:js` - Minify JavaScript files
- `npm run optimize:images` - Optimize image files
- `npm run clean` - Remove minified files
- `npm run deploy` - Build and deploy to GitHub Pages

## Tech Stack

- **HTML5** - Semantic markup
- **Bootstrap 4** - Responsive grid and components
- **Vanilla JavaScript** + **jQuery 3.7.1** - Interactive functionality
- **CSS3** with custom properties - Modern styling
- **WOW.js** - Scroll animations
- **Font Awesome** - Icon library

## Project Structure

```
tianshufu.github.io/
├── index.html              # Main portfolio page
├── videos_speach.html      # Speech competition video
├── videos_sport.html       # Basketball match video
├── assets/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── img/               # Images and photos
│   ├── fonts/             # Icon fonts
│   └── files/             # Downloadable files (resume)
├── package.json           # NPM dependencies and scripts
└── README.md             # This file
```

## Performance Improvements

Before optimizations:
- 23 JavaScript libraries loaded (~404 KB)
- jQuery 3.2.1 (2017)
- No lazy loading
- Inline scripts in HTML

After optimizations:
- Removed 1 unused library (MixItUp)
- jQuery 3.7.1 (latest)
- Lazy loading on images
- Modernized code with ES6+
- CSS variables for easy theming
- Consolidated and clean codebase

## License

MIT License - Feel free to fork and use this template for your own portfolio!

## Author

**Tianshu Fu**
- LinkedIn: [tianshu-fu](https://www.linkedin.com/in/tianshu-fu-696a58181)
- GitHub: [tianshufu](https://github.com/tianshufu)
- Email: tf2502@columbia.edu
