import Vue from 'vue';
import Router from 'vue-router';
import Currencies from './components/Currencies.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Currencies',
      component: Currencies,
    },
  ],
});
