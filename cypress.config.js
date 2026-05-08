module.exports = {
  e2e: {
    setupNodeEvents(on, config) {},
    baseUrl: 'http://localhost:8000',
    supportFile: 'cypress/support/index.js',
    specPattern: 'cypress/e2e/**/*.{cy.js,test.js}',
  },
};
